import json

from sqlalchemy.orm import Session

from app.ai.hf_client import HuggingFaceClient
from app.db.models import Interview, Question
from app.services.context_service import ContextService


class AdaptiveQuestionService:

    def __init__(self):
        self.llm = HuggingFaceClient()
        self.context_service = ContextService()

    def generate_next_question(
        self,
        db: Session,
        interview: Interview,
    ) -> Question:

        history = (
            self.context_service
            .get_interview_history(
                db,
                interview.id,
            )
        )

        next_sequence = len(history) + 1

        prompt = f"""
You are conducting an adaptive technical interview.

Topic:
{interview.topic}

Difficulty:
{interview.difficulty}

Interview history:
{json.dumps(history, indent=2)}

Your task is to generate the NEXT interview question.

Rules:

1. Do not repeat previous questions.
2. Analyze the candidate's previous answers.
3. Target an important weakness or missing concept.
4. If the candidate performed strongly,
   increase the difficulty.
5. If the candidate performed poorly,
   test the missing fundamentals.
6. Ask exactly ONE question.
7. Do not provide the answer.

Return ONLY the question.
"""

        question_text = self.llm.generate(prompt)

        question = Question(
            interview_id=interview.id,
            question=question_text.strip(),
            sequence=next_sequence,
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        return question