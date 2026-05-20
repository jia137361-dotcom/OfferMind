from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from .base import BaseModel


class Question(BaseModel):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(20), default="medium", index=True)
    tags = Column(JSONB, nullable=True)
    reference_answer = Column(Text, nullable=True)
    key_points = Column(JSONB, nullable=True)
    embedding = Column(Vector(1024), nullable=True)
    source = Column(String(100), default="manual")
    is_active = Column(Boolean, default=True, index=True)
