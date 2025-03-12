from pydantic import BaseModel, Field
from typing import Optional



class Payment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    task_id: str 
    client_id: str  
    receiver_id: str  
    total_amount: int
  
    status: str = "pending" 

  
class Paymentcreate(BaseModel):
    task_id : str
    receiver_id: str
    total_amount: int
    status: str = "pending" 
    
