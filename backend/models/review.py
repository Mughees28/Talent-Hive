from pydantic import BaseModel, Field
from typing import Optional



class Review(BaseModel):
    id: Optional[str] = Field(None, alias="_id") 
    task_id: str  
    reviewer_id: str  
    reviewee_id: str  
    rating: float  
    feedback: Optional[str] = None  

    