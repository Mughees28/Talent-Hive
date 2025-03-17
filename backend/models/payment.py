from pydantic import BaseModel, Field
from typing import Optional


  
class Paymentcreate(BaseModel):
    task_id : str
    receiver_id: str
    total_amount: int
    status: str = "pending" 

class Agencypayment(BaseModel):
    task_id : str
    
    status: str = "pending" 
    
