import uuid
from typing import Optional
from datetime import date, datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from backend.logic.enum import UserStatus, UserTypes


class User(SQLModel, table=True):
    full_name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    birth_date: date
    gender: str

    user_status: UserStatus = Field(default=UserStatus.ACTIVE)
    user_type: UserTypes = Field(default=UserTypes.EXTERNAL)
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)

    profile: Optional["Profile"] = Relationship(back_populates="user")
    