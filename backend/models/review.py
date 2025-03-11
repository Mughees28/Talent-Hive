from pydantic import BaseModel, Field, conint
from typing import Optional



class Review(BaseModel):
    id: Optional[str] = Field(None, alias="_id") 
    task_id: str  
    reviewer_id: str  
    reviewee_id: str  
    rating: float  
    feedback: Optional[str] = None  


class Reviewcreate(BaseModel):
    task_id: str 
    reviewee_id:str
    rating: conint(ge=1, le=5) 
    comment: Optional[str] = None