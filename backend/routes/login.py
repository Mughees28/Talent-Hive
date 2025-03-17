from datetime import timedelta
from oauth2 import create_access_token
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import users_collection
from config import  verify_password
from models.user import Userlogin
from database import users_collection



router = APIRouter()


@router.post("/login")
async def login(user: Userlogin):
   
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user["password"]):
         raise HTTPException(status_code=400, detail="Invalid email or password")

    

    access_token = create_access_token(data={"sub": user.email})
    user_data= {"id": str(db_user["_id"]),
            "name": db_user["name"],
            "email": db_user["email"],
            "role": db_user["role"]}
    if db_user["role"] == "agency_owner":
        user_data["agency_name"]=db_user["agency_name"]
    return {"token": access_token, "token_type": "bearer",
            "user":user_data}


