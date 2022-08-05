from fastapi import FastAPI
from app.routers import employee, person, department

app = FastAPI()

app.include_router(employee.router)
app.include_router(person.router)
app.include_router(department.router)