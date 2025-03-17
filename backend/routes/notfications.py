from fastapi import APIRouter, Depends, HTTPException
from models.notification import NotificationCreate
from database import notifications_collection
from bson import ObjectId

router = APIRouter(prefix="/notifications")

@router.post("/")
async def create_notification(notification: NotificationCreate):
    new_notification = {
        "user_id": ObjectId(notification.user_id),
        "message": notification.message,
        "task_id": ObjectId(notification.task_id) if notification.task_id else None
    }
    notifications_collection.insert_one(new_notification)
    return {"message": "Notification created successfully"}

@router.get("/{user_id}")
async def get_notifications(user_id: str):
    notifications = list(notifications_collection.find({"user_id": ObjectId(user_id)}))
    
    for notification in notifications:
        notification["_id"] = str(notification["_id"])
        notification["user_id"] = str(notification["user_id"])
        if notification.get("task_id"):
            notification["task_id"] = str(notification["task_id"])

    return {"notifications": notifications}

@router.delete("/{user_id}/clear")
async def clear_notifications(user_id: str):
    notifications_collection.delete_many({"user_id": ObjectId(user_id)})
    return {"message": "All notifications cleared"}
