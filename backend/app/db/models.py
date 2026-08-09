from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Interview(Base):

    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    candidate_name: Mapped[str] = mapped_column(
        String(100)
    )

    topic: Mapped[str] = mapped_column(
        String(100)
    )

    difficulty: Mapped[str] = mapped_column(
        String(50),
        default="medium",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    questions = relationship(
        "Question",
        back_populates="interview",
        cascade="all, delete-orphan",
    )


class Question(Base):

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id")
    )

    question: Mapped[str] = mapped_column(
        Text
    )

    sequence: Mapped[int] = mapped_column(
        Integer
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    interview = relationship(
        "Interview",
        back_populates="questions",
    )

    answer = relationship(
        "Answer",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Answer(Base):

    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id")
    )

    answer: Mapped[str] = mapped_column(
        Text
    )

    score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    weaknesses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    missing_concepts: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    follow_up_question: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    question = relationship(
        "Question",
        back_populates="answer",
    )