from sqlalchemy.orm import Session

from app.db.models import Interview


class InterviewSessionService:

    def create_interview(
        self,
        db: Session,
        candidate_name: str,
        topic: str,
        difficulty: str = "medium",
    ) -> Interview:

        interview = Interview(
            candidate_name=candidate_name,
            topic=topic,
            difficulty=difficulty,
        )

        db.add(interview)
        db.commit()
        db.refresh(interview)

        return interview
    
    def get_interview(
        self,
        db: Session,
        interview_id: int,
    ) -> Interview | None:

        interview = db.get(Interview, interview_id)

        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")

        return interview