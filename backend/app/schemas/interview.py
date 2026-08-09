from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    topic: str
    
class AnswerRequest(BaseModel):
    question: str
    answer: str


class Evaluation(BaseModel):
    score: int = Field(ge=0, le=10)
    strengths: list[str]
    weaknesses: list[str]
    missing_concepts: list[str]
    follow_up_question: str
    
class InterviewCreateRequest(BaseModel):
    candidate_name: str
    topic: str
    difficulty: str = "medium"
    
class AnswerSubmission(BaseModel):
    answer: str