import json

from sqlalchemy.orm import Session

from app.ai.hf_client import HuggingFaceClient
from app.db.models import Answer, Question
from app.schemas.interview import Evaluation


class AnswerService:

    def __init__(self):
        self.llm = HuggingFaceClient()

    def submit_answer(
        self,
        db: Session,
        question: Question,
        answer_text: str,
    ) -> Answer:

        evaluation = self._evaluate(
            question.question,
            answer_text,
        )

        answer = Answer(
            question_id=question.id,
            answer=answer_text,
            score=evaluation.score,
            strengths=json.dumps(evaluation.strengths),
            weaknesses=json.dumps(evaluation.weaknesses),
            missing_concepts=json.dumps(
                evaluation.missing_concepts
            ),
            follow_up_question=evaluation.follow_up_question,
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)

        return answer

    def _evaluate(
        self,
        question: str,
        answer: str,
    ) -> Evaluation:

        prompt = f"""
You are a senior technical interviewer.

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate the answer.

Return ONLY valid JSON:

{{
    "score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_concepts": [],
    "follow_up_question": ""
}}

Scoring:
0-3 = Poor
4-5 = Below average
6-7 = Good
8-9 = Strong
10 = Exceptional
"""

        raw = self.llm.generate(prompt)

        data = json.loads(raw)

        return Evaluation(**data)