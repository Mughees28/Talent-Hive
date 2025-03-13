from fastapi import FastAPI
from database import db
from routes import signup, login, tasks,bids, users, reviews, payments
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(tasks.router)
app.include_router(bids.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(payments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    collections = db.list_collection_names()
    return {"message": "MongoDB Atlas connected!", "collections": collections}
