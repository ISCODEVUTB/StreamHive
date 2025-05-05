import uuid
from typing import Optional
from datetime import date, datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from backend.logic.enum import UserStatus, UserTypes, UserGender


class User(SQLModel, table=True):
    """
    Database model for a user.

    Attributes:
        full_name (str): Full name of the user (max 255 characters).
        email (EmailStr): Unique email address of the user, indexed for fast lookup.
        hashed_password (str): Hashed password for authentication purposes.
        birth_date (date): User's date of birth.
        user_gender (str): User's gender (max 20 characters typically).
        user_status (UserStatus): Current status of the user (active, inactive, deleted).
        user_type (UserTypes): Type of user (internal or external).
        user_id (UUID): Primary key identifier, auto-generated UUID.
        created_at (datetime): Timestamp of when the user account was created (UTC time).
        profile (Optional["Profile"]): Optional one-to-one relationship to the user's profile.
    """
    full_name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    birth_date: date
    user_gender: UserGender

    user_status: UserStatus = Field(default=UserStatus.ACTIVE)
    user_type: UserTypes = Field(default=UserTypes.EXTERNAL)
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)

    profile: Optional["Profile"] = Relationship(back_populates="user")
    