from typing import Optional
import uuid
from datetime import date
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from backend.logic.enum import UserStatus, UserGender, UserTypes

class UserBase(SQLModel):
    """
    Base model for user data containing common fields.

    Attributes:
        full_name (Optional[str]): The user's full name, up to 255 characters.
        email (EmailStr): The user's email address, validated as a proper email.
        user_type (Optional[UserTypes]): The type of user (internal or external).
    """
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=255)
    user_type: Optional[UserTypes] = None
    user_gender: UserGender | None


class CreateUser(UserBase):
    """
    Model for creating a new user, extending UserBase with additional fields.

    Attributes:
        password (str): User's password (8-16 characters).
        birth_date (date): User's date of birth.
        gender (str): User's gender, up to 20 characters.
    """
    password: str = Field(min_length=8, max_length=16)
    birth_date: date


class RegisterUser(SQLModel):
    """
    Model used specifically for user registration (public-facing).

    Attributes:
        full_name (str): Full name of the registering user.
        email (EmailStr): Email address of the registering user.
        birth_date (date): Date of birth.
        gender (str): Gender of the user.
        password (str): Password (8-16 characters).
    """
    full_name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    birth_date: date
    user_gender: UserGender
    password: str = Field(min_length=8, max_length=16)


class UpdateUser(UserBase):
    """
    Model for updating a user's details (admin use).

    Attributes:
        password (Optional[str]): Updated password, if provided.
        email (Optional[EmailStr]): Updated email address, if provided.
        gender (Optional[str]): Updated gender, if provided.
        user_status (Optional[UserStatus]): Updated user status (active, inactive, deleted).
    """
    password: Optional[str] = Field(default=None, min_length=8, max_length=16)
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    user_gender: UserGender | None = None
    user_status: Optional[UserStatus] = None


class UpdateLogged(SQLModel):
    """
    Model for updating logged-in user's own information.

    Attributes:
        full_name (Optional[str]): Updated full name.
        email (Optional[EmailStr]): Updated email address.
        gender (Optional[str]): Updated gender.
    """
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    user_gender: UserGender | None = None

class UpdatePassword(SQLModel):
    """
    Model for updating a user's password.

    Attributes:
        current_password (Optional[str]): The user's current password.
        new_password (Optional[str]): The new password to be set.
    """
    current_password: str | None = Field(default=None, min_length=8, max_length=16)
    new_password: str | None = Field(default=None, min_length=8, max_length=16)


class UserPublic(UserBase):
    """
    Public-facing model for exposing user data safely.

    Attributes:
        user_id (uuid.UUID): Unique identifier for the user.
        birth_date (date): User's date of birth.
        gender (str): User's gender.
        user_status (UserStatus): Current status of the user.
    """
    user_id: uuid.UUID
    birth_date: date
    user_gender: str
    user_status: UserStatus

class UsersPublic(SQLModel):
    """
    Model representing a paginated list of public users.

    Attributes:
        users (List[UserPublic]): List of user public profiles.
        count (int): Total number of users matching a query or in the system.
    """
    users: list[UserPublic]
    count: int