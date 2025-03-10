from pydantic import BaseModel, Field
from typing import Optional



class Bid(BaseModel):
    id: Optional[str] = Field(None, alias="_id") 
    task_id: str 
    bidder_id: str  
    amount: float  
    status: str = "pending"  

class BidCreate(BaseModel):
    task_id: str  
    amount: float  
      
