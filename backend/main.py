from fastapi import FastAPI
from database import db

app = FastAPI()

@app.get("/")
def home():
    collections = db.list_collection_names()
    return {"message": "MongoDB Atlas connected!", "collections": collections}
