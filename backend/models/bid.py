from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Bid Schema
class Bid(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ID
    task_id: str  # ID of the task being bid on
    bidder_id: str  # Freelancer or Agency ID
    amount: float  # Bid amount
    message: str  # Optional bid message
    status: str = "pending"  # "pending", "accepted", "rejected"

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
