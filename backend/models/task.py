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
    class Config:
        orm_mode = True

class Taskcreate(BaseModel):
    title: str
    description: str
    budget: int
    deadline: str

    class Config:
        orm_mode = True
   
class Taskupdate(BaseModel):
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    is_approved: Optional[bool] = None

   
class SubTaskcreate(BaseModel):
    task_id: str
    description: str
    deadline: str
    assigned_to: str