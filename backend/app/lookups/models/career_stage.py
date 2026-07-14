from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class CareerStage(Base):
    __tablename__ = "career_stages"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="career_stage")