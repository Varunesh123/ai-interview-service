from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json

from app.config import settings
from app.schemas.interview import (
    QuestionRequest, 
    AnswerRequest, 
    InterviewCreateRequest, 
    AnswerSubmission
)
from app.db.database import get_db
from app.db.models import Question

from app.services.interview_service import InterviewService
from app.services.evaluation_service import EvaluationService
from app.services.question_service import QuestionService
from app.services.answer_service import AnswerService
from app.services.interview_session_service import InterviewSessionService

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

interview_service = InterviewService()
evaluation_service = EvaluationService()
interview_session_service = InterviewSessionService()
question_service = QuestionService()
answer_service = AnswerService()


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
    
@app.post("/interviews/{interview_id}/start")
async def start_interview(
    interview_id: int,
    db: Session = Depends(get_db),
):

    interview = interview_session_service.get_interview(
        db,
        interview_id,
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found",
        )
    
    existing_question = question_service.get_first_question(
        db,
        interview.id,
    )

    if existing_question:
        return {
            "interview_id": interview.id,
            "question_id": existing_question.id,
            "sequence": existing_question.sequence,
            "question": existing_question.question,
        }

    question = question_service.generate_first_question(
        db=db,
        interview=interview,
    )

    return {
        "interview_id": interview.id,
        "question_id": question.id,
        "sequence": question.sequence,
        "question": question.question,
    }
    
@app.post("/questions/{question_id}/answer")
async def submit_answer(
    question_id: int,
    request: AnswerSubmission,
    db: Session = Depends(get_db),
):

    question = db.get(Question, question_id)

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    answer = answer_service.submit_answer(
        db=db,
        question=question,
        answer_text=request.answer,
    )

    return {
        "question_id": question.id,
        "score": answer.score,
        "strengths": json.loads(answer.strengths),
        "weaknesses": json.loads(answer.weaknesses),
        "missing_concepts": json.loads(
            answer.missing_concepts
        ),
        "follow_up_question": answer.follow_up_question,
    }