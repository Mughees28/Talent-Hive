from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import users_collection
from models.user import Usersignup
from config import hash_password 
from typing import Optional



router = APIRouter()




@router.post("/signup")
async def register(user: Usersignup):
   
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"]=hash_password(user.password)
    
    
    
    users_collection.insert_one(user_dict)

    return {"message": "User registered successfully"}


