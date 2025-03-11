from fastapi import APIRouter, HTTPException,Depends
from models.review import Reviewcreate
from database import tasks_collection,reviews_collection
from oauth2 import get_current_user
from bson import ObjectId



router = APIRouter(prefix="/reviews")

@router.post("/")
async def submit_review(review: Reviewcreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["freelancer","agency","client"]:
        raise HTTPException(status_code=403, detail="Agency freelancer can't leave a review")

    
    task = tasks_collection.find_one({"_id": ObjectId(review.task_id)})

    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if str(task["_id"]) == review.task_id:
        raise HTTPException(status_code=403, detail="Review already exist")
    
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before reviewing")
    
    if task["is_approved"] != True:
        raise HTTPException(status_code=400, detail="Task must be approved before reviewing")

   
    if task.get("assigned_to") != review.reviewee_id:
        raise HTTPException(status_code=400, detail="Freelancer was not assigned to this task")

    review_dict = review.dict()
    review_dict["reviewer_id"] = current_user["_id"] 

    inserted_review = reviews_collection.insert_one(review_dict)

    response_review = review_dict.copy()
    response_review["_id"] = str(inserted_review.inserted_id)
    response_review["reviewer_id"] = str(response_review["reviewer_id"])
    response_review["reviewee_id"] = str(response_review["reviewee_id"])

    return {"message": "Review submitted successfully", "review": response_review}



@router.get("/{reviewee_id}")
async def get_reviews_by_id(reviewee_id: str, current_user: dict = Depends(get_current_user)):
    reviews = list(reviews_collection.find({"reviewee_id": reviewee_id}))

    for review in reviews:
        review["_id"] = str(review["_id"])
        review["reviewer_id"] = str(review["reviewer_id"])
        review["reviewee_id"] = str(review["reviewee_id"])
        review["task_id"] = str(review["task_id"])
        


    return {"freelancer_id": reviewee_id, "reviews": reviews}
