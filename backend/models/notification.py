from pydantic import BaseModel
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: str  # The recipient of the notification
    message: str  # Notification content
    task_id: Optional[str] = None  # Optional task reference
