from fastapi import FastAPI

from app.database.base import Base
from app.database.session import engine

# Import models
from app.users.models.user import User
from app.lookups.models.career_stage import CareerStage

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Interview Preparation System"
)


@app.get("/")
def home():
    return {
        "message": "Backend is running successfully."
    }