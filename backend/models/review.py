from pydantic import BaseModel, Field, conint
from typing import Optional


class Reviewcreate(BaseModel):
    task_id: str 
    reviewee_id:str
    rating: conint(ge=1, le=5) 
    comment: Optional[str] = None