import json

from app.ai.hf_client import HuggingFaceClient
from app.schemas.interview import Evaluation


class EvaluationService:

    def __init__(self):
        self.llm = HuggingFaceClient()

    def evaluate(
        self,
        question: str,
        answer: str,
    ) -> Evaluation:

        prompt = f"""
You are a senior technical interviewer.

Evaluate the candidate's answer.

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate:

1. Technical correctness
2. Depth of understanding
3. Important concepts covered
4. Missing concepts
5. Engineering reasoning

Return ONLY valid JSON.

Required format:

{{
    "score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_concepts": [],
    "follow_up_question": ""
}}

Rules:

- score must be an integer from 0 to 10
- strengths must be an array of strings
- weaknesses must be an array of strings
- missing_concepts must be an array of strings
- follow_up_question must be a string
- Do not include markdown
- Do not include explanations outside JSON
"""

        raw_response = self.llm.generate(prompt)

        data = json.loads(raw_response)

        return Evaluation(**data)