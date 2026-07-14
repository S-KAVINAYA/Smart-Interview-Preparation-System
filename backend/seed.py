from app.users.models.user import User
from app.database.session import SessionLocal
from app.lookups.models.career_stage import CareerStage

db = SessionLocal()

career_stages = [
    "Student",
    "Graduate",
    "Working Professional"
]

for stage in career_stages:

    existing_stage = db.query(CareerStage).filter(
        CareerStage.name == stage
    ).first()

    if not existing_stage:
        db.add(
            CareerStage(name=stage)
        )

db.commit()
db.close()

print("Career stages seeded successfully.")