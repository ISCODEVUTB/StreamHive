from typing import Optional
import uuid
from datetime import date
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from backend.logic.enum.user_status import UserStatus
from backend.logic.enum.user_types import UserTypes

class UserBase(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=255)
    user_type: Optional[UserTypes] = None


class CreateUser(UserBase):
    password: str = Field(min_length=8, max_length=16)
    birth_date: date
    gender: str = Field(max_length=20)


class RegisterUser(SQLModel):
    full_name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    birth_date: date
    gender: str = Field(max_length=20)
    password: str = Field(min_length=8, max_length=16)


class UpdateUser(UserBase):
    password: Optional[str] = Field(default=None, min_length=8, max_length=16)
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    gender: Optional[str] = Field(default=None, max_length=20)
    user_status: Optional[UserStatus] = None


class UpdateLogged(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    gender: str | None = Field(default=None, max_length=20)


class UpdatePassword(SQLModel):
    current_password: str | None = Field(default=None, min_length=8, max_length=16)
    new_password: str | None = Field(default=None, min_length=8, max_length=16)


class UserPublic(UserBase):
    user_id: uuid.UUID
    birth_date: date
    gender: str
    user_status: UserStatus

class UsersPublic(SQLModel):
    users: list[UserPublic]
    count: int