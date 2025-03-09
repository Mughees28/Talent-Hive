from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Review Schema
class Review(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ID
    task_id: str  # Related task ID
    reviewer_id: str  # Who is giving the review
    reviewee_id: str  # Who is receiving the review
    rating: float  # Rating out of 5
    feedback: Optional[str] = None  # Optional feedback message

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
