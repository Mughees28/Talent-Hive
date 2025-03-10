from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    id: Optional[str] = Field(None, alias="_id") 
    title: str
    description: str
    budget: int
    deadline: str  
    client_id: str  
    assigned_to: Optional[str] = None  
    status: str = "open"  

class Taskcreate(BaseModel):
    title: str
    description: str
    budget: int
    deadline: str
   
   
   
