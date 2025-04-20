# Feel free to edit whatever you need. Just wanted to get it set up so that I can integrate this with the AJAX later on - Christian 
# Names collection in firestore "signed-in" - Julie
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
import datetime
from typing import Annotated

# Define literatls for attendance due date at 6 PM
HOUR = 18  # must be in 24 hour format
MINUTE = 0

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# initalize firestore client
db = firestore.Client()
student_collection = db.collection("signed-in")

# for testing purposes
students_signed_in = [
    {"name": "Student 1", "time": "12:00 PM", "attendance": True},  
    {"name": "Student 2", "time": "12:05 PM", "attendance": True},
    {"name": "Student 3", "time": "12:10 PM", "attendance": True},
]

@app.get("/")
async def read_root(request: Request):
    signed_in = student_collection.stream()
    students_signed_in = []
    
    for s in signed_in:
        students_signed_in.append(s.to_dict())
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "students_signed_in": students_signed_in
    })
    
@app.post("/")
async def create_sign_in(name: Annotated[str, Form()]):
    # check sign in time
    time  = datetime.datetime.utcnow()
    class_start = datetime.datetime.combine(time.date(), datetime.time(HOUR, MINUTE))

    # add attendance to database
    student_collection.add({
        "name": name,
        "time": time.isoformat(),
        "attendance": time > class_start
    })
    
    return {"message": f"Sign in for {name} received!"}