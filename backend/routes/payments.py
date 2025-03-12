from fastapi import APIRouter, HTTPException,Depends
from models.payment import Paymentcreate
from database import tasks_collection,payments_collection, users_collection
from oauth2 import get_current_user
from bson import ObjectId

router =APIRouter(prefix="/payments")


@router.post("/")
async def post_payments(payment:Paymentcreate, current_user: dict = Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(payment.task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before making payment")
    
    if task["is_approved"] != True:
        raise HTTPException(status_code=400, detail="Task must be approved before making payment")
    
    if task.get("assigned_to") != payment.receiver_id:
        raise HTTPException(status_code=400, detail="Freelancer/Agency was not assigned to this task")


    # if payment.status != "pending":
    #     raise HTTPException(status_code=403, detail="Already paid")
    existing_payment = payments_collection.find_one({"task_id": payment.task_id})
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment already exists for this task")

   
   
    payment_dict = payment.dict()
    payment_dict["client_id"] = current_user["_id"]
    payment_dict["task_id"] = ObjectId(current_user["task_id"])
    payment_dict["receiver_id"] = ObjectId(current_user["receiver_id"])
    
    

    inserted_review = payments_collection.insert_one(payment_dict)
    
    

    response_review = payment_dict.copy()
    response_review["_id"] = str(inserted_review.inserted_id)
    response_review["client_id"] = str(response_review["client_id"])
    response_review["receiver_id"] = str(response_review["receiver_id"])

    return {"message": "Payment added successfully", "reciept": response_review}


@router.get("/{user_id}")
async def get_payment_by_user(user_id:str, current_user: dict = Depends(get_current_user)):

    
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0}) 

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # print(user["role"])


    if user["role"]=="client":
         payments = list(payments_collection.find({"client_id": user_id}))

    else:
         payments = list(payments_collection.find({"receiver_id": user_id}))
        #  print(len(payments))

    
    total_amount = sum(payment["total_amount"] for payment in payments)

    return {"total_amout":total_amount}
        

@router.get("/task_id}")
async def calculate_commision(task_id:str, current_user: dict = Depends(get_current_user)):
    
