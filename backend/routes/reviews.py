from fastapi import APIRouter, HTTPException,Depends
from models.review import Reviewcreate
from database import tasks_collection,reviews_collection,users_collection
from oauth2 import get_current_user
from bson import ObjectId



router = APIRouter(prefix="/reviews")

@router.post("/")
async def submit_review(review: Reviewcreate, current_user: dict = Depends(get_current_user)):

    if current_user["role"] not in ["freelancer", "client","agency_owners"]:
        raise HTTPException(status_code=403, detail="Only clients and freelancers can leave a review")

    task = tasks_collection.find_one({"_id": ObjectId(review.task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_review = reviews_collection.find_one({"task_id": ObjectId(review.task_id), "reviewee_id": review.reviewee_id})
    if existing_review:
        raise HTTPException(status_code=403, detail="Review already exists for this task")

    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed before reviewing")

    if not task.get("is_approved", False):
        raise HTTPException(status_code=400, detail="Task must be approved before reviewing")

    
    if str(task.get("assigned_to")) != review.reviewee_id:
        raise HTTPException(status_code=400, detail="Freelancer/Agency was not assigned to this task")

  
    review_dict = review.dict()
    review_dict["reviewer_id"] = str(current_user["_id"]) 

    inserted_review = reviews_collection.insert_one(review_dict)
    review_dict["_id"] = str(inserted_review.inserted_id) 
    return {"message": "Review submitted successfully", "review": review_dict}


@router.get("/{reviewee_id}")
async def get_reviews_by_id(reviewee_id: str, current_user: dict = Depends(get_current_user)):
    reviewee = users_collection.find_one({"_id": ObjectId(reviewee_id)})
    if not reviewee:
        raise HTTPException(status_code=404, detail="User not found")

    reviews = list(reviews_collection.find({"reviewee_id": reviewee_id}))

    for review in reviews:
        for key in ["_id", "reviewer_id", "reviewee_id", "task_id"]:
            review[key] = str(review[key])

    if reviews:
        average_rating = sum(r["rating"] for r in reviews) / len(reviews)
        average_rating = round(average_rating, 2)
    else:
        average_rating = 0

    return {
        "reviewee_id": reviewee_id,
        "average_rating": average_rating,
        "reviews": reviews
    }
