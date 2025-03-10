from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from models.bid import BidCreate 
from database import tasks_collection,users_collection,bids_collection
from oauth2 import get_current_user
from bson import ObjectId


router =APIRouter(prefix="/bids")

@router.post("/")
async def place_bid(bid: BidCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["freelancer","agency"]:
        raise HTTPException(status_code=403, detail="Only freelancers and agency owners can place bids")

    task = tasks_collection.find_one({"_id": ObjectId(bid.task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    bid_dict = bid.dict()
    bid_dict["freelancer_id"] = current_user["_id"]  

    inserted_bid = bids_collection.insert_one(bid_dict)
    bid_dict["_id"] = str(inserted_bid.inserted_id)  

    return {"message": "Bid placed successfully", "bid": bid_dict}