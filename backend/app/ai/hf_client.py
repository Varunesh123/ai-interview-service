from huggingface_hub import InferenceClient

from app.config import settings


class HuggingFaceClient:

    def __init__(self):
        self.client = InferenceClient(
            api_key=settings.huggingface_api_key
        )

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model="Qwen/Qwen3-4B-Instruct-2507",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=500,
        )

        return response.choices[0].message.content