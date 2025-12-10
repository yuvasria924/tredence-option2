# app/schemas.py
from pydantic import BaseModel


class SummarizeBody(BaseModel):
    text: str
    max_length: int = 200


class CodeReviewBody(BaseModel):
    code: str
    threshold: int = 7  # desired quality_score (0-10)
