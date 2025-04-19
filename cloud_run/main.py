# Feel free to edit whatever you need. Just wanted to get it set up so that I can integrate this with the AJAX later on - Christian 
# Names collection in firestore "signed-in" - Julie
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
import datetime
from typing import Annotated

app = FastAPI()

# make sure to also mount any static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# init firestore client
db = firestore.Client()
student_collection = db.collection("signed-in")

# for testing purposes
students_signed_in = [
    {"name": "Student 1", "time": "12:00 PM"},  
    {"name": "Student 2", "time": "12:05 PM"},
    {"name": "Student 3", "time": "12:10 PM"},
]

@app.get("/")
async def read_root(request: Request):
    signed_in = student_collection.stream()
    # @note: we are storing the votes in `vote_data` list because the firestore stream closes after certain period of time
    students_signed_in = []
    
    for s in signed_in:
        students_signed_in.append(s.to_dict())
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "students_signed_in": students_signed_in
    })
    
@app.post("/")
async def create_vote(name: Annotated[str, Form()]):

    student_collection.add({
        "name": name,
        "time": datetime.datetime.utcnow().isoformat()
    })
    
    return {"message": f"Sign in for {name} received!"}