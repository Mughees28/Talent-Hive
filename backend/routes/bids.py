from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from models.bid import BidCreate 
from database import tasks_collection,bids_collection,users_collection
from oauth2 import get_current_user
from bson import ObjectId


router =APIRouter(prefix="/bids")

@router.post("/")
async def place_bid(bid: BidCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["freelancer","agency_owner"]:
        raise HTTPException(status_code=403, detail="Only freelancers and agency owners can place bids")

    task = tasks_collection.find_one({"_id": ObjectId(bid.task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    bid_dict = bid.dict()
    bid_dict["bidder_id"] = ObjectId(current_user["_id"])  
    bid_dict["task_id"] = ObjectId(bid.task_id)
  
    bid_dict["name"] = current_user["name"]


    inserted_bid = bids_collection.insert_one(bid_dict) 
    response_bid = bid_dict.copy()
    response_bid["_id"] = str(inserted_bid.inserted_id)
    response_bid["bidder_id"] = str(response_bid["bidder_id"])
    response_bid["task_id"] = str(response_bid["task_id"])

    return {"message": "Bid placed successfully","bid":response_bid}


@router.get("/{bid_id}")
async def get_bid(bid_id: str, current_user: dict = Depends(get_current_user)):
    bid = bids_collection.find_one({"_id": ObjectId(bid_id)})
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    
   
    bid["_id"] = str(bid["_id"])
    bid["bidder_id"] = str(bid["bidder_id"]) 
    bid["task_id"] = str(bid["task_id"])
    
    return bid

@router.get("/task/{task_id}")
async def get_bids_by_task(task_id: str, current_user: dict = Depends(get_current_user)):
    bids = list(bids_collection.find({"task_id": ObjectId(task_id)}))
    
 
    for bid in bids:
        bid["_id"] = str(bid["_id"])
        bid["bidder_id"] = str(bid["bidder_id"])
        bid["task_id"] = str(bid["task_id"])
    
    
    return bids


@router.delete("/{bid_id}")
async def delete_bid(bid_id: str, current_user: dict = Depends(get_current_user)):
    bid = bids_collection.find_one({"_id": ObjectId(bid_id)})
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    
 
    if str(bid["bidder_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this bid")
    
    result = bids_collection.delete_one({"_id": ObjectId(bid_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bid not found")
    
    return {"message": "Bid deleted successfully"}

@router.put("/{bid_id}/approve")
async def approve_bid(bid_id: str, current_user: dict = Depends(get_current_user)):
    
    bid = bids_collection.find_one({"_id": ObjectId(bid_id)})
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    task = tasks_collection.find_one({"_id": ObjectId(bid["task_id"])})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["client_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to approve this bid")

    bids_collection.update_one({"_id": ObjectId(bid_id)}, {"$set": {"status": "approved"}})

    tasks_collection.update_one(
        {"_id": ObjectId(bid["task_id"])},
        {"$set": {"assigned_to": str(bid["bidder_id"]), "status": "in_progress"}}
    )

    bids_collection.update_many(
        {"task_id": ObjectId(bid["task_id"]), "_id": {"$ne": ObjectId(bid_id)}},
        {"$set": {"status": "rejected"}}
    )

    return {"message": "Bid approved successfully, task assigned to bidder"}