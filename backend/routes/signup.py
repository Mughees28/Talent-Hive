from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import users_collection
from config import hash_password 



router = APIRouter()



class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  
    agency_id: str = None  



@router.post("/signup")
async def register(user: UserSignup):
   
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"]=hash_password(user.password)
    
    
    
    users_collection.insert_one(user_dict)

    return {"message": "User registered successfully"}


