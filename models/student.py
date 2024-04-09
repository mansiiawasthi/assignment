from pydantic import BaseModel

class Address(BaseModel):
    city: str | None = None
    country: str | None = None

class Student(BaseModel):
    name: str | None = None
    age: int | None = None
    address: Address | None = None