# Feel free to edit whatever you need. Just wanted to get it set up so that I can integrate this with the AJAX later on - Christian 

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# make sure to also mount any static files
templates = Jinja2Templates(directory="app/templates")

# for testing purposes
students_signed_in = [
    {"name": "Student 1", "time": "12:00 PM"},  
    {"name": "Student 2", "time": "12:05 PM"},
    {"name": "Student 3", "time": "12:10 PM"},
]

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "students_signed_in": students_signed_in
    })