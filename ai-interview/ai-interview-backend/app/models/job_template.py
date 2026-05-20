from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from .base import BaseModel


class JobTemplate(BaseModel):
    __tablename__ = "job_templates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    required_skills = Column(JSONB, nullable=True)
    preferred_skills = Column(JSONB, nullable=True)
    responsibilities = Column(JSONB, nullable=True)
    question_categories = Column(JSONB, nullable=True)
    difficulty_level = Column(String(20), default="medium")
    is_active = Column(Boolean, default=True, index=True)
