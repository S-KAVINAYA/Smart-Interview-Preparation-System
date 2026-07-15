from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.sql import func

from app.database.base import Base


class VerificationCode(Base):

    __tablename__ = "verification_codes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    verification_type = Column(
        String(30),
        nullable=False
    )

    code = Column(
        String(10),
        nullable=False
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    is_used = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )