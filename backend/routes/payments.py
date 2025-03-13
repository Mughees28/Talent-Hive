from fastapi import APIRouter, HTTPException, Depends
from models.payment import Paymentcreate
from database import tasks_collection, payments_collection, users_collection, bids_collection
from oauth2 import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/payments")

@router.post("/")
async def post_payments(payment: Paymentcreate, current_user: dict = Depends(get_current_user)):
   
    task = tasks_collection.find_one({"_id": ObjectId(payment.task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

 
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before making payment")
    
    if not task.get("is_approved"):
        raise HTTPException(status_code=400, detail="Task must be approved before making payment")

    
    existing_payment = payments_collection.find_one({"task_id": payment.task_id})
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment already exists for this task")

    
    bid = bids_collection.find_one({"task_id": ObjectId(payment.task_id), "status": "approved"})
    if not bid:
        raise HTTPException(status_code=404, detail="No approved bid found for this task")

    total_amount = bid["amount"]  

    
    assigned_to = task.get("assigned_to")

    payment_records = []  

    
    freelancer = users_collection.find_one({"_id": ObjectId(assigned_to), "role": "freelancer"})
    if freelancer:
        payment_records.append({
            "task_id": ObjectId(payment.task_id),
            "client_id": ObjectId(current_user["_id"]),
            "receiver_id": ObjectId(assigned_to),  
            "total_amount": total_amount,
            "status": "paid"
        })

   
    agency = users_collection.find_one({"_id": ObjectId(assigned_to), "role": "agency_owner"})
    if agency:
        agency_cut = total_amount * 0.40  
        freelancer_cut = total_amount * 0.60  

       
        agency_freelancers = list(users_collection.find({"agency_id": assigned_to, "role": "freelancer"}))
        freelancer_count = len(agency_freelancers)

        if freelancer_count > 0:
            per_freelancer_payment = freelancer_cut / freelancer_count  

            
            payment_records.append({
                "task_id": ObjectId(payment.task_id),
                "client_id": ObjectId(current_user["_id"]),
                "receiver_id": ObjectId(assigned_to), 
                "total_amount": agency_cut,
                "status": "paid"
            })

          
            for freelancer in agency_freelancers:
                payment_records.append({
                    "task_id": ObjectId(payment.task_id),
                    "client_id": ObjectId(current_user["_id"]),
                    "receiver_id": ObjectId(freelancer["_id"]),
                    "total_amount": per_freelancer_payment,
                    "status": "paid"
                })

    if payment_records:
        payments_collection.insert_many(payment_records)
        return {"message": "Payments processed successfully", "payments": payment_records}
    
    return {"message": "No valid payments to process"}

@router.get("/{client_id}/spending")
async def get_client_spending(client_id: str, current_user: dict = Depends(get_current_user)):
   
    client = users_collection.find_one({"_id": ObjectId(client_id)}, {"password": 0})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if client["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients have spending records")

    spendings = list(payments_collection.find({"client_id": ObjectId(client_id)}))

    for payment in spendings:
        payment["_id"] = str(payment["_id"])
        payment["task_id"] = str(payment["task_id"])
        payment["client_id"] = str(payment["client_id"])
        payment["receiver_id"] = str(payment["receiver_id"])

   
    total_spent = sum(payment["total_amount"] for payment in spendings)

    return {
        "client_id": client_id,
        "total_spent": total_spent,
        "transactions": spendings
    }

@router.get("/{user_id}/earnings")
async def get_user_earnings(user_id: str, current_user: dict = Depends(get_current_user)):
    
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

   
    if user["role"] not in ["freelancer", "agency_owner"]:
        raise HTTPException(status_code=403, detail="Only freelancers or agencies have earnings records")

    
    earnings = list(payments_collection.find({"receiver_id": ObjectId(user_id)}))

   
    for payment in earnings:
        payment["_id"] = str(payment["_id"])
        payment["task_id"] = str(payment["task_id"])
        payment["client_id"] = str(payment["client_id"])
        payment["receiver_id"] = str(payment["receiver_id"])

  
    total_earned = sum(payment["total_amount"] for payment in earnings)

    return {
        "user_id": user_id,
        "total_earned": total_earned,
        "transactions": earnings
    }
