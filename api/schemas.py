from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Текст ответа")


class AnswerCreate(AnswerBase):
    user_id: Optional[UUID] = None


class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Текст вопроса")


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    answers: Optional[List[AnswerResponse]] = []

    class Config:
        from_attributes = True
