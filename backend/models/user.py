from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class Usersignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  
    agency_name: Optional[str] = None  
    

class Userlogin(BaseModel):

    email: str
    password: str

class AddFreelancer(BaseModel):
    name: str
    email: EmailStr
    password: str
    skill: str
    role: str= "agency_freelancer"