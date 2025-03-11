from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from models.task import Taskcreate,Taskupdate,Taskapproved
from database import tasks_collection,users_collection
from oauth2 import get_current_user
from bson import ObjectId




router = APIRouter(prefix="/tasks")

@router.post("/")
async def createTask(task : Taskcreate,current_user: dict = Depends(get_current_user)):

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


@router.get("/{task_id}")
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task["_id"] = str(task["_id"])  
    task["client_id"] = str(task["client_id"])

    return task


@router.delete("/{task_id}")
async def get_tasks(id:str, current_user: dict = Depends(get_current_user)):
     task = tasks_collection.find_one({"_id": ObjectId(id)})
     if not task:
        raise HTTPException(status_code=404, detail="Task not found")

     if task["client_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this task")

     tasks_collection.delete_one({"_id": ObjectId(id)})
 
     return {"message": "Task deleted successfully"}




@router.put("/{user_id}")
async def get_posted_task(task_id: str, update_data: Taskupdate, current_user: dict = Depends(get_current_user)):

    if task["client_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to update this task")

    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

   
   
    update_dict = update_data.dict(exclude_none=True)

  
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_dict})

    return {"message": "Task updated successfully"}


@router.put("/approve/{task_id}")
async def update_task_approved(task_id: str, current_user: dict = Depends(get_current_user)):
    
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["client_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to approve this task")

  
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before approving")

   
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"is_approved": True}})

    return {"message": "Task approved successfully"}