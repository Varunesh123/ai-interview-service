from app.ai.hf_client import HuggingFaceClient


class InterviewService:

    def __init__(self):
        self.llm = HuggingFaceClient()

    def generate_question(self, topic: str) -> str:

        prompt = f"""
You are a senior software engineer conducting
a technical interview.

Generate ONE interview question about:

{topic}

Requirements:
- Ask a practical question
- Avoid trivial definitions
- The question should test engineering understanding
- Do not provide the answer

Return only the question.
"""

        return self.llm.generate(prompt)