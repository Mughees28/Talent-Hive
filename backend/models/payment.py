from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Payment Schema
class Payment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ID
    task_id: str  # Task related to payment
    client_id: str  # ID of the client paying
    receiver_id: str  # Freelancer or Agency Owner receiving payment
    total_amount: float  # Full amount
    commission_percentage: Optional[float] = 0.0  # Commission (if agency)
    commission_amount: Optional[float] = 0.0  # Calculated commission
    final_amount: float  # Amount after commission deduction
    status: str = "pending"  # "pending", "completed"

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
