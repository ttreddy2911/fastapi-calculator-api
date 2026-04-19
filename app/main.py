from fastapi import FastAPI

from app.database import Base, engine
from app.routers import users, calculations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Calculator API",
    description="FastAPI backend with user authentication and calculation CRUD endpoints",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(calculations.router)


@app.get("/")
def root():
    return {"message": "Calculator API is running"}