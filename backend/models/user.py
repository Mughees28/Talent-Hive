from pydantic import BaseModel, EmailStr, Field
from typing import Optional



def to_object_id(id: str) -> ObjectId:
    return ObjectId(id)


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    name: str
    email: EmailStr
    password: str 
    role: str 
    agency_id: Optional[str] = None  
    class Config:
        orm_mode = True

    