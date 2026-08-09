from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.services.interview_service import InterviewService
from app.services.evaluation_service import EvaluationService
from app.schemas.interview import QuestionRequest, AnswerRequest, InterviewCreateRequest
from app.db.database import get_db
from app.services.interview_session_service import (
    InterviewSessionService,
)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

interview_service = InterviewService()
evaluation_service = EvaluationService()
interview_session_service = InterviewSessionService()

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

@app.post("/interviews")
async def create_interview(
    request: InterviewCreateRequest,
    db: Session = Depends(get_db),
):

    interview = interview_session_service.create_interview(
        db=db,
        candidate_name=request.candidate_name,
        topic=request.topic,
        difficulty=request.difficulty,
    )

    return {
        "id": interview.id,
        "candidate_name": interview.candidate_name,
        "topic": interview.topic,
        "difficulty": interview.difficulty,
        "status": interview.status,
    }