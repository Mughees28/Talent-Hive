from fastapi import APIRouter, HTTPException, Depends
from database import users_collection
from oauth2 import get_current_user
from bson import ObjectId
from models.user import AddFreelancer
from config import hash_password 

router = APIRouter(prefix="/users")



@router.get("/")
async def get_all_users(current_user: dict = Depends(get_current_user)):
   
   
    users = list(users_collection.find({}, {"password": 0}))  

    for user in users:
        user["_id"] = str(user["_id"])  

    return {"users": users}

@router.get("/get-freelancer")
async def get_agencyFreelancer( current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "agency_owner":
        raise HTTPException(status_code=403, detail="Not Authenticated to get freelancer")
    
    users = list(users_collection.find({"agency_id":current_user["_id"]}, {"password": 0}))  

    for user in users:
        user["_id"] = str(user["_id"])  
        user["agency_id"] = str(user["agency_id"])  

    return {"users": users}


@router.get("/{user_id}")
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0}) 

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])  
    return user


@router.post("/addfreelancer")
async def add_agencyFreelancer(freelancer: AddFreelancer, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "agency_owner":
        raise HTTPException(status_code=403, detail="Not Authenticated to add freelancer")
    
    existing_user = users_collection.find_one({"email": freelancer.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = freelancer.dict()
    user_dict["password"]=hash_password(freelancer.password)
    
    users_collection.insert_one(user_dict)

    return {"message": "Agency Freelancer registered successfully"}


@router.post("/deletefreelancer/{freelancer_id}")
async def add_agencyFreelancer(freelancer_id: str, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "agency_owner":
        raise HTTPException(status_code=403, detail="Not Authenticated to delete freelancer")
    
    user = users_collection.find_one({"_id": ObjectId(freelancer_id)})
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    users_collection.delete_one({"email": freelancer_id.email})
   

    return {"message": "Agency Freelancer deleted successfully"}

