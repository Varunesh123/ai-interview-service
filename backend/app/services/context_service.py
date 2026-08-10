from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Interview, Question


class ContextService:

    def get_interview_history(
        self,
        db: Session,
        interview_id: int,
    ) -> list[dict]:

        questions = db.scalars(
            select(Question)
            .where(
                Question.interview_id == interview_id
            )
            .order_by(Question.sequence)
        ).all()

        history = []

        for question in questions:

            item = {
                "question": question.question,
                "sequence": question.sequence,
            }

            if question.answer:
                item["answer"] = question.answer.answer
                item["score"] = question.answer.score
                item["missing_concepts"] = (
                    question.answer.missing_concepts
                )

            history.append(item)

        return history