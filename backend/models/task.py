from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Task Schema
class Task(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ID
    title: str
    description: str
    budget: float
    deadline: str  # Store deadline as a string (ISO format)
    client_id: str  # ID of the client who posted
    assigned_to: Optional[str] = None  # Freelancer/Agency ID
    status: str = "open"  # "open", "assigned", "completed"

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
