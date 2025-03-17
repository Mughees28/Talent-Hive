from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from models.task import Taskcreate,Taskupdate,SubTaskcreate
from database import tasks_collection,users_collection,notifications_collection
from oauth2 import get_current_user
from bson import ObjectId




router = APIRouter(prefix="/tasks")

@router.post("/createtask")
async def createTask(task : Taskcreate,current_user: dict = Depends(get_current_user)):

    if current_user["role"] !="client":
        raise HTTPException(status_code=403, detail="Only Clients can create tasks")

    task_dict = task.dict()
    
    task_dict["client_id"] = current_user["_id"] 
    task_dict["status"] = "open"
    
    tasks_collection.insert_one(task_dict)

    return {"message": "Task added successfully"}

    

@router.get("/")
async def get_tasks(current_user: dict = Depends(get_current_user)):
 
    if current_user["role"] not in ["client", "freelancer", "agency_owner"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
        
    tasks = list(tasks_collection.find())
        
  
    for task in tasks:
        task["_id"] = str(task["_id"])
        
        if "client_id" in task and task["client_id"]:
            task["client_id"] = str(task["client_id"])
    
    return {"data": tasks}

@router.post("/addsubtask")
async def create_sub_Task(task :SubTaskcreate ,current_user: dict = Depends(get_current_user)):
    
    
    if current_user["role"] != "agency_owner":
        raise HTTPException(status_code=403, detail="Not Authenticated to Create subtask")
    
    parent_task = tasks_collection.find_one({"_id": ObjectId(task.task_id)})
    if not parent_task:
        raise HTTPException(status_code=404, detail="Parent task not found")

    
    subtask_dict = task.dict()
    
    subtask_dict["agency_id"] = current_user["_id"] 
    subtask_dict["category"] = "subtask"
    
    tasks_collection.insert_one(subtask_dict)
    notifications_collection.insert_one({
        "user_id": task.assigned_to,
        "message": f"You have been assigned a new subtask: {task.title}",
    
    })

    return {"message": "sub-Task added successfully"}

@router.get("/getsubtask")
async def get_completed_subtask(current_user: dict = Depends(get_current_user)):
    
    
    if current_user["role"] != "agency_owner":
        raise HTTPException(status_code=403, detail="Not Authenticated to get completed subtask")
    if current_user["role"] == "agency_owner":
        tasks = list(tasks_collection.find({
            # "status": "assigned",
            "agency_id": current_user["_id"],
            "category": "subtask"
        }))
    else:
        tasks = list(tasks_collection.find({
            "status": "assigned",
            "assigned_to": current_user["_id"],
            "category": "subtask"
        }))

    if not tasks:
        raise HTTPException(status_code=404, detail="No Assigned tasks found")
    
    for task in tasks:
        task["_id"] = str(task["_id"])
        task["agency_id"] = str(task["agency_id"])
        if "assigned_to" in task and task["assigned_to"]:
            task["assigned_to"] = str(task["assigned_to"])


    return {"tasks": tasks}


@router.get("/available")
async def get_available_task(current_user: dict = Depends(get_current_user)):
    
    if current_user["role"] != "client":
        tasks = list(tasks_collection.find({
            "status": "open"
        }))
   
    
    
    for task in tasks:
        task["_id"] = str(task["_id"])
        task["client_id"] = str(task["client_id"])
        if "assigned_to" in task and task["assigned_to"]:
            task["assigned_to"] = str(task["assigned_to"])


    return {"tasks": tasks}

@router.get("/assigned")
async def get_assigned_task(current_user: dict = Depends(get_current_user)):
    
    if current_user["role"] == "client":
        tasks = list(tasks_collection.find({
            "status": "assigned",
            "client_id": current_user["_id"]
        }))
    else:
        tasks = list(tasks_collection.find({
            "status": "assigned",
            "assigned_to": str(current_user["_id"]),
            
        }))

    total_assigned = len(tasks)
    print("in assigned")
    print(total_assigned)

    # if not tasks:
    #     raise HTTPException(status_code=404, detail="No Assigned tasks found")
    
    for task in tasks:
        task["_id"] = str(task["_id"])
        if "assigned_to" in task and task["assigned_to"]:
            task["assigned_to"] = str(task["assigned_to"])

        if current_user["role"] == "agency_freelancer":
             task["agency_id"] = str(task["agency_id"])
        elif current_user["role"] in ["agency_owner","freelancer","client"] :
            task["client_id"] = str(task["client_id"])
    
    # notification = {
    #     "user_id": task["assigned_to"],
    #     "message": f"You have been assigned a new task: {task['title']}."
    # }
    # notifications_collection.insert_one(notification)

    return {"tasks": tasks,"total_assigned":total_assigned}

@router.get("/posted")
async def get_posted_task(current_user: dict = Depends(get_current_user)):
    tasks=[]
    if current_user["role"] == "client":
        tasks = list(tasks_collection.find({
            "client_id": current_user["_id"]
        }))

    # if not tasks:
    #     raise HTTPException(status_code=404, detail="No Posted tasks found")
    total_posted = len(tasks)
    for task in tasks:
        task["_id"] = str(task["_id"])
        task["client_id"] = str(task["client_id"])
        if "assigned_to" in task and task["assigned_to"]:
            task["assigned_to"] = str(task["assigned_to"])

    return {"tasks": tasks,"total_posted":total_posted}


@router.get("/completed")
async def get_completed_task(current_user: dict = Depends(get_current_user)):
    print("in completed")
    if current_user["role"] == "client":
        tasks = list(tasks_collection.find({
            "status": "completed",
            "client_id": current_user["_id"]
        }))

    
    else:
        tasks = list(tasks_collection.find({
            "status": "completed",
            "assigned_to": str(current_user["_id"])
        }))
    total_completed = len(tasks)
    print(total_completed)

    # if not tasks:
    #     raise HTTPException(status_code=404, detail="No completed tasks found")
    
    for task in tasks:
        task["_id"] = str(task["_id"])
       

        if "assigned_to" in task and task["assigned_to"]:
            task["assigned_to"] = str(task["assigned_to"])

        if current_user["role"] == "agency_freelancer":
             task["agency_id"] = str(task["agency_id"])
        elif current_user["role"] in ["agency_owner","freelancer","client"] :
            task["client_id"] = str(task["client_id"])
    notification = {
        "user_id": task["client_id"],
        "message": f"Your task '{task['title']}' has been marked as completed."
    }
    notifications_collection.insert_one(notification)


    return {"tasks": tasks,"total_completed":total_completed}



@router.get("/{task_id}")
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task["_id"] = str(task["_id"])  

    if current_user["role"] == "agency_freelancer":
             task["agency_id"] = str(task["agency_id"])
    elif current_user["role"] in ["agency_owner","freelancer","client"] :
            task["client_id"] = str(task["client_id"])

    return task


@router.delete("/{task_id}")
async def delete_tasks(task_id:str, current_user: dict = Depends(get_current_user)):
    
     task = tasks_collection.find_one({"_id": ObjectId(task_id)})
     if not task:
        raise HTTPException(status_code=404, detail="Task not found")

     if task["client_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this task")

     tasks_collection.delete_one({"_id": ObjectId(id)})
 
     return {"message": "Task deleted successfully"}




@router.put("/{task_id}")
async def update_posted_task(task_id: str, update_data: Taskupdate, current_user: dict = Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 🔒 Authorization check
    if current_user["role"] in ["agency_freelancer", "agency_owner", "freelancer"] and task["assigned_to"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Unauthorized to update this task")
    elif current_user["role"] == "client" and task["client_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to update this task")

    update_dict = update_data.dict(exclude_none=True)
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_dict})

    # 🔔 Notifications
    if "assigned_to" in update_dict and update_dict["assigned_to"]:
        notifications_collection.insert_one({
            "user_id": ObjectId(update_dict["assigned_to"]),
            "message": f"You have been assigned a new task: {task['title']}",
            
        })

    if "status" in update_dict and update_dict["status"] == "completed":
        notifications_collection.insert_one({
            "user_id": ObjectId(task["client_id"]),
            "message": f"Your task '{task['title']}' has been marked as completed.",
            
        })

    if "is_approved" in update_dict and update_dict["is_approved"]:
        notifications_collection.insert_one({
            "user_id": ObjectId(task["assigned_to"]),
            "message": f"Your task '{task['title']}' has been approved!",
          
        })

    if "is_paid" in update_dict and update_dict["is_paid"]:
        notifications_collection.insert_one({
            "user_id": ObjectId(task["assigned_to"]),
            "message": f"Payment has been made for your task: {task['title']}",
          
        })

    return {"message": "Task updated successfully"}


@router.put("/{task_id}/approve")
async def approve_task(task_id: str, current_user: dict = Depends(get_current_user)):
    
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["client_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to approve this task")

  
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before approving")

   
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"is_approved": True}})

    return {"message": "Task approved successfully"}


