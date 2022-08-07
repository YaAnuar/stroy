import uvicorn
from fastapi import FastAPI
from app.config.db import init_db
from app.routers import employee, person, department

app = FastAPI()

app.include_router(employee.router)
app.include_router(person.router)
app.include_router(department.router)

@app.on_event("startup")
async def startup_event():
    await init_db()