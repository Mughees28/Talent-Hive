from pydantic import BaseModel, Field
from typing import Optional



class BidCreate(BaseModel):
    task_id: str  
    amount: float  
    status: str = "pending"  
