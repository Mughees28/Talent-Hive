from datetime import timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import users_collection
from models.user import Usersignup
from config import hash_password
from oauth2 import create_access_token  

router = APIRouter()

@router.post("/signup")
async def register(user: Usersignup):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

 
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    
    users_collection.insert_one(user_dict)

  
    access_token = create_access_token(data={"sub": user.email})

 
    user_data = {
        "id": str(user_dict["_id"]),
        "name": user_dict["name"],
        "email": user_dict["email"],
        "role": user_dict["role"]
    }

    if user_dict["role"] == "agency_owner":
        user_data["agency_name"] = user_dict["agency_name"]

    return {
        "message": "User registered successfully",
        "token": access_token,
        "token_type": "bearer",
        "user": user_data
    }
