from fastapi import FastAPI
from app.verification.models import VerificationCode
from app.database.base import Base
from app.database.session import engine
from app.verification.routes import router as verification_router
# Import models
from app.users.models.user import User
from app.lookups.models.career_stage import CareerStage
from app.auth.routes import router as auth_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Interview Preparation System"
)
app.include_router(auth_router)
app.include_router(verification_router)

@app.get("/")
def home():
    return {
        "message": "Backend is running successfully."
    }