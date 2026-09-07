from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base


class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255))

    questions = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan")


class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"))
    question = Column(Text)
    opt1 = Column(String(255))
    opt2 = Column(String(255))
    opt3 = Column(String(255))
    opt4 = Column(String(255))
    correct_ans = Column(Integer)

    exam = relationship("Exam", back_populates="questions")


class ExamHistory(Base):
    __tablename__ = "exam_histories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"))
    score = Column(Integer)
    total = Column(Integer)
    wrong_details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    exam = relationship("Exam")