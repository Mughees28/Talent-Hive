from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

# Helper function to convert MongoDB ObjectId to string
def to_object_id(id: str) -> ObjectId:
    return ObjectId(id)

# User Schema
class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ID
    name: str
    email: EmailStr
    password: str  # Hashed password
    role: str  # "client", "freelancer", "agency_owner", "agency_freelancer"
    agency_id: Optional[str] = None  # Only for agency freelancers

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
