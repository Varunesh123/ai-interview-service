from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings
from app.services.interview_service import InterviewService
from app.services.evaluation_service import EvaluationService
from app.schemas.interview import QuestionRequest, AnswerRequest


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

interview_service = InterviewService()
evaluation_service = EvaluationService()

@app.get("/")
async def home():
    return {
        "Home": "Welcome to the Interview API",
    }

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
    
@app.post("/interview/evaluate")
async def evaluate_answer(request: AnswerRequest):

    evaluation = evaluation_service.evaluate(
        question=request.question,
        answer=request.answer,
    )

    return evaluation