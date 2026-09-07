from typing import Any
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class ExamImport(BaseModel):
    title: str = Field(..., max_length=255)
    raw_text: str

    @field_validator('title')
    @classmethod
    def check_title(cls, v):
        if not v or not str(v).strip():
            raise HTTPException(status_code=400, detail="Tên bài thi không được để trống")
        return str(v).strip()

    @field_validator('raw_text')
    @classmethod
    def check_exam_content(cls, v):
        if not v or not str(v).strip():
            raise HTTPException(status_code=400, detail="Nội dung bài thi không được để trống")

        lines = str(v).strip().split('\n')
        valid_count = 0
        for line in lines:
            if not line.strip():
                continue
            if len(line.split('|')) == 6:
                valid_count += 1

        if valid_count < 1:
            raise HTTPException(status_code=400, detail="Bài thi phải có tối thiểu 1 câu hỏi hợp lệ (có đủ 6 phần cách nhau bởi dấu |)")
        return str(v)


class ExamHistoryCreate(BaseModel):
    score: int
    total: int
    wrong_details: Any


class ExamHistoryOut(ExamHistoryCreate):
    id: int
    exam_id: int
    created_at: datetime

    class Config:
        from_attributes = True