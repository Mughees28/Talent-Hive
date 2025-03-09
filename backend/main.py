from fastapi import FastAPI
from database import db
from .routers import login, signup

app = FastAPI()

app.include_router(login.router)
app.include_router(signup.router)

@app.get("/")
def home():
    collections = db.list_collection_names()
    return {"message": "MongoDB Atlas connected!", "collections": collections}
