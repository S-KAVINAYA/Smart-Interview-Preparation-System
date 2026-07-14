from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    mobile_number = Column(String(15), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    career_stage_id = Column(
        Integer,
        ForeignKey("career_stages.id"),
        nullable=False
    )

    email_verified = Column(Boolean, default=False)

    mobile_verified = Column(Boolean, default=False)

    account_status = Column(String(30), default="Pending Verification")

    login_provider = Column(String(20), default="EMAIL")

    profile_completed = Column(Boolean, default=False)

    profile_completion_percentage = Column(Integer, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    last_login = Column(DateTime(timezone=True), nullable=True)

    career_stage = relationship(
        "CareerStage",
        back_populates="users"
    )