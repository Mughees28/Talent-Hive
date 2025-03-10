from fastapi import FastAPI
from database import db
from routes import signup, login, tasks,bids



app = FastAPI()

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(tasks.router)
app.include_router(bids.router)


@app.get("/")
def home():
    collections = db.list_collection_names()
    return {"message": "MongoDB Atlas connected!", "collections": collections}
