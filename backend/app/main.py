from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings
from app.services.interview_service import InterviewService


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

interview_service = InterviewService()


class QuestionRequest(BaseModel):
    topic: str


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
    }


@app.post("/interview/question")
async def generate_question(request: QuestionRequest):

    question = interview_service.generate_question(
        request.topic
    )

    return {
        "topic": request.topic,
        "question": question,
    }