import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "courses.json")

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

def load_courses():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_courses(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/courses")
def get_courses():
    courses = load_courses()
    return courses


@app.post("/courses")
def create_course(course: Course):
    courses = load_courses()
    courses.append(course.model_dump())      
    save_courses(courses)                
    return {"message": "Course added successfully", "added_course": course}

@app.get("/")
def root():
    return {"message": "FastAPI Course Record Server is running."}