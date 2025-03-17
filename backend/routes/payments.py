from fastapi import APIRouter, HTTPException, Depends
from models.payment import Paymentcreate,Agencypayment
from database import tasks_collection, payments_collection, users_collection, bids_collection
from oauth2 import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/payments")

@router.post("/")
async def post_payments(payment: Paymentcreate, current_user: dict = Depends(get_current_user)):
    print("In post payment")
   
 
    task = tasks_collection.find_one({"_id": ObjectId(payment.task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before making payment")
    
    if not task.get("is_approved"):
        raise HTTPException(status_code=400, detail="Task must be approved before making payment")

    existing_payment = payments_collection.find_one({"task_id": ObjectId(payment.task_id)})
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment already exists for this task")

    print("In post payment 2")

    total_amount = int(task.get("selectedbid_amount"))  
    print(total_amount)
    if not total_amount:
        raise HTTPException(status_code=400, detail="No payment amount found for this task")

    assigned_to = task.get("assigned_to")
    if not assigned_to:
        raise HTTPException(status_code=400, detail="Task is not assigned to anyone")

    payment_records = []

    
  
   
   
    user = users_collection.find_one({"_id": ObjectId(assigned_to)})
    if user:
        print("in user")
      
        payment_records.append({
            "task_id": ObjectId(payment.task_id),
            "client_id": current_user["_id"],
            "receiver_id": ObjectId(assigned_to),  
            "total_amount": total_amount,
            "status": "paid",
       
        })

  
    # agency = users_collection.find_one({"_id": ObjectId(assigned_to), "role": "agency_owner"})
    # if agency and current_user["role"]== "agency_owner":
    #     print("In agency")
    #     agency_cut = total_amount * 0.40  
    #     freelancer_cut = total_amount * 0.60  

     
    #     agency_freelancers = list(users_collection.find({"agency_id": assigned_to, "role": "agency_freelancer"}))
    #     freelancer_count = len(agency_freelancers)

    #     if freelancer_count > 0:
    #         per_freelancer_payment = freelancer_cut / freelancer_count  

           
    #         payment_records.append({
    #             "task_id": ObjectId(payment.task_id),
    #             "client_id": ObjectId(current_user["_id"]),
    #             "receiver_id": ObjectId(assigned_to),  
    #             "total_amount": agency_cut,
    #             "status": "paid",
    #             "role": "agency_owner"
    #         })

           
    #         for freelancer in agency_freelancers:
    #             payment_records.append({
    #                 "task_id": ObjectId(payment.task_id),
    #                 "client_id": ObjectId(current_user["_id"]),
    #                 "receiver_id": ObjectId(freelancer["_id"]),
    #                 "total_amount": per_freelancer_payment,
    #                 "status": "paid",
    #                 "role": "agency_freelancer"
    #             })
    #     elif agency:
    #         payment_records.append({
    #         "task_id": ObjectId(payment.task_id),
    #         "client_id": ObjectId(current_user["_id"]),
    #         "receiver_id": ObjectId(assigned_to),  
    #         "total_amount": total_amount,
    #         "status": "paid",
    #         "role": "agency_owner"
    # })

    
    if payment_records:
        payments_collection.insert_many(payment_records)
        print("payment added")
        tasks_collection.update_one({"_id": ObjectId(payment.task_id)}, {"$set": {"is_paid": True}})
        print("is paid added")
        return {"message": "Payments processed successfully"}
    
    return {"message": "No valid payments to process"}

@router.get("/earnings/{user_id}")
async def get_user_earnings(user_id: str, current_user: dict = Depends(get_current_user)):
   
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

   
    if user["role"] in ["freelancer", "agency_owner","agency_freelancer"]:
        earnings = list(payments_collection.find({"receiver_id": ObjectId(user_id)}))

    else:
         print("in client")
         earnings = list(payments_collection.find({"client_id": ObjectId(user_id)}))
    

    print(earnings)
    for payment in earnings:
        payment["_id"] = str(payment["_id"])
        payment["task_id"] = str(payment["task_id"])
        payment["client_id"] = str(payment["client_id"])
        payment["receiver_id"] = str(payment["receiver_id"])

  
    total_earned = sum(payment["total_amount"] for payment in earnings)
    # print(user["agency_name"])

    return {
        "user_id": user_id,
        "total_earned": total_earned,
        "transactions": earnings
    }
@router.get("/task/{task_id}")
async def get_user_earnings(user_id: str, current_user: dict = Depends(get_current_user)):
   
    user = users_collection.find_one({"_id": current_user}, {"password": 0})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

   
    if user["role"] in ["agency_owner"]:
        earnings = list(payments_collection.find({"receiver_id": ObjectId(user_id)}))

    else:
         print("in client")
         earnings = list(payments_collection.find({"client_id": ObjectId(user_id)}))
    

    print(earnings)
    for payment in earnings:
        payment["_id"] = str(payment["_id"])
        payment["task_id"] = str(payment["task_id"])
        payment["client_id"] = str(payment["client_id"])
        payment["receiver_id"] = str(payment["receiver_id"])

  
    total_earned = sum(payment["total_amount"] for payment in earnings)
    # print(user["agency_name"])

    return {
        "user_id": user_id,
        "total_earned": total_earned,
        "transactions": earnings
    }

@router.post("/agency-payments")
async def post_payments(payment: Agencypayment, current_user: dict = Depends(get_current_user)):
    print("In post payment")
   
    # Fetch the main task
    task = tasks_collection.find_one({"_id": ObjectId(payment.task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before making payment")
    print("completed")
    
    if not task.get("is_approved"):
        raise HTTPException(status_code=400, detail="Task must be approved before making payment")
    print("approved")
    ispaid =task["is_paid"]
    print(ispaid)
    if ispaid != True:
        raise HTTPException(status_code=400, detail="Task payment already processed")
    print("is paid")
    total_amount = int(task.get("selectedbid_amount"))  
    print("Total Payment:", total_amount)
    
    if not total_amount:
        raise HTTPException(status_code=400, detail="No payment amount found for this task")
    print("not total amount")

    assigned_to = task.get("assigned_to")
    if not assigned_to:
        raise HTTPException(status_code=400, detail="Task is not assigned to anyone")

    # Get all completed subtasks for this task
    subtasks = list(tasks_collection.find({
        "task_id": str(task["_id"]),
        "category": "subtask",
        "status": "completed"
    }))

    if not subtasks:
        raise HTTPException(status_code=400, detail="No completed subtasks found for payment processing.")

    freelancer_count = len(subtasks)
    freelancer_cut = total_amount * 0.60  # 60% for freelancers
    agency_cut = total_amount * 0.40  # 40% for agency owner

    if freelancer_count > 0:
        per_freelancer_payment = freelancer_cut / freelancer_count  

        # Pay the agency owner
        payments_collection.insert_one({
            "task_id": ObjectId(payment.task_id),
            "client_id": ObjectId(current_user["_id"]),
            "receiver_id": ObjectId(assigned_to),  
            "total_amount": agency_cut,
            "status": "paid",
            "role": "agency_owner"
        })

        # Pay each freelancer who worked on the subtask
        for subtask in subtasks:
            freelancer_id = subtask["assigned_to"]
            payments_collection.insert_one({
                "task_id": ObjectId(payment.task_id),
                "client_id": ObjectId(current_user["_id"]),
                "receiver_id": ObjectId(freelancer_id),
                "total_amount": per_freelancer_payment,
                "status": "paid",
                "role": "agency_freelancer"
            })

            # ✅ **Mark the subtask as paid**
            tasks_collection.update_one(
                {"_id": subtask["_id"]}, 
                {"$set": {"is_paid": True}}
            )
    final_agency_payment = total_amount - freelancer_cut 

        # ✅ **Update Agency Owner's Existing Payment Record**
    payments_collection.delete_one(
            {
                "task_id": ObjectId(payment.task_id),
                "receiver_id": ObjectId(assigned_to),  
            
            }
    
        )
    payments_collection.insert_one(
            {
                "task_id": ObjectId(payment.task_id),
                "client_id": ObjectId(current_user["_id"]),
                "receiver_id": ObjectId(assigned_to),  
                "total_amount": final_agency_payment,
                "status": "paid",
                "role": "agency_owner",
                
                
            })
    # ✅ **Mark the main task as paid**
    tasks_collection.update_one({"_id": ObjectId(payment.task_id)}, {"$set": {"is_paid": True}})

    return {"message": "Payments processed successfully"}
