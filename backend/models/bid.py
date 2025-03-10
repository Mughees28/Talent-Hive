from pydantic import BaseModel, Field
from typing import Optional



class Bid(BaseModel):
    id: Optional[str] = Field(None, alias="_id") 
    task_id: str 
    bidder_id: str  
    amount: float  
    message: str  
    status: str = "pending"  

    
