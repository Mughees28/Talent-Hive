from pydantic import BaseModel, Field
from typing import Optional


class Taskcreate(BaseModel):
    title: str
    description: str
    budget: int
    deadline: str

    
   
class Taskupdate(BaseModel):
    assigned_to: Optional[str] = None
    status: Optional[str] = "open"
    is_approved: Optional[bool] = None
    is_paid: Optional[bool] = None
    selectedbid_amount: Optional[int] = None

   
class SubTaskcreate(BaseModel):
    task_id: str
    description: str
    deadline: str
    assigned_to: str
    status: str="open"