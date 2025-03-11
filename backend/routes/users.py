from fastapi import APIRouter, HTTPException, Depends
from database import users_collection
from oauth2 import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/users")



@router.get("/")
async def get_all_users(current_user: dict = Depends(get_current_user)):
   
   
    users = list(users_collection.find({}, {"password": 0}))  

    for user in users:
        user["_id"] = str(user["_id"])  

    return {"users": users}



@router.get("/{user_id}")
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0}) 

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])  
    return user