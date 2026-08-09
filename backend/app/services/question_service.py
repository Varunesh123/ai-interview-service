from sqlalchemy.orm import Session
from sqlalchemy import select

from app.ai.hf_client import HuggingFaceClient
from app.db.models import Interview, Question


class QuestionService:

    def __init__(self):
        self.llm = HuggingFaceClient()

    def generate_first_question(
        self,
        db: Session,
        interview: Interview,
    ) -> Question:

        prompt = f"""
You are a senior technical interviewer.

Conduct an interview on:

Topic: {interview.topic}
Difficulty: {interview.difficulty}

Generate the FIRST interview question.

Rules:
- Ask one practical engineering question.
- Do not ask a basic definition.
- The question should allow the candidate
  to explain their reasoning.
- Do not provide the answer.
- Return ONLY the question.
"""

        question_text = self.llm.generate(prompt)

        question = Question(
            interview_id=interview.id,
            question=question_text.strip(),
            sequence=1,
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        return question
    
    def get_first_question(
        self,
        db: Session,
        interview_id: int,
    ) -> Question | None:

        return db.scalar(
            select(Question)
            .where(
                Question.interview_id == interview_id,
                Question.sequence == 1,
            )
        )