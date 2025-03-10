from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from models.task import Taskcreate
from database import tasks_collection,users_collection
from oauth2 import get_current_user




router = APIRouter(prefix="/tasks")

@router.post("/")
def createTask(task : Taskcreate,user_email: str = Depends(get_current_user)):

    task_dict = task.dict()
    current_user = users_collection.find_one({"email": user_email})
    task_dict["client_id"] = current_user["_id"] 
    task_dict["status"] = "open"
    
    tasks_collection.insert_one(task_dict)

    return {"message": "Task added successfully"}

@router.get("/")
def getTask():

    
    task_dict = list(tasks_collection.find())
    
    
    tasks = list(tasks_collection.find({}, {"_id": 0}))
    

    return {"message": "Task fetched successfully","data":tasks}



