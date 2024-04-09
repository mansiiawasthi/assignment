from fastapi import HTTPException, Query, APIRouter
from bson import ObjectId
from models.student import Student
from config.database import collection_name

router = APIRouter()

@router.post("/students", status_code=201)
async def create_student(student: Student):
    student_data = student.model_dump()
    inserted_student = collection_name.insert_one(student_data)
    return {"id": str(inserted_student.inserted_id)}

@router.get("/students", status_code=200)
async def get_students(country: str = Query(None), age: int = Query(None)):
    filters = {}
    if country:
        filters["address.country"] = country
    if age:
        filters["age"] = {"$gte": age}

    students = list(collection_name.find(filters, {"_id": 0}))
    return {"data": students}

@router.get("/students/{id}", status_code=200)
async def get_student(id: str):
    student = collection_name.find_one({"_id": ObjectId(id)}, {"_id": 0})
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")


@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student_update: Student):
    # Check if student exists
    student = collection_name.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Extract the fields to be updated
    student_data = student_update.model_dump(exclude_unset=True)
    if not student_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Update the student in the database
    updated_student = collection_name.update_one(
        {"_id": ObjectId(id)},
        {"$set": student_data}
    )
    return {}
   

@router.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    deleted_student = collection_name.delete_one({"_id": ObjectId(id)})
    if deleted_student.deleted_count:
        return {}
    raise HTTPException(status_code=404, detail="Student not found")