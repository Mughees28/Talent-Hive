from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import users_collection
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User Signup Model
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "client", "freelancer", "agency_owner", "agency_freelancer"
    agency_id: str = None  # Only if role is "agency_freelancer"

# User Login Model
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT tokens
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ------------------------ SIGNUP ROUTE ------------------------
@router.post("/register")
async def register(user: UserSignup):
    # Check if user already exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password before saving
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    
    # Insert user into MongoDB
    users_collection.insert_one(user_dict)

    return {"message": "User registered successfully"}

# ------------------------ LOGIN ROUTE ------------------------
# @router.post("/login")
# async def login(user: UserLogin):
#     # Find user by email
#     db_user = users_collection.find_one({"email": user.email})
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Invalid email or password")

#     # Verify password
#     if not verify_password(user.password, db_user["password"]):
#         raise HTTPException(status_code=400, detail="Invalid email or password")

#     # Generate JWT Token
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

#     return {"access_token": access_token, "token_type": "bearer"}
