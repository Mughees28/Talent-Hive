from pydantic import BaseModel
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: str  
    message: str  
    task_id: Optional[str] = None  
