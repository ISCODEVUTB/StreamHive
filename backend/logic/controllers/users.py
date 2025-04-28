from typing import Any

from sqlmodel import Session, select

from backend.core.security import get_password_hash
from backend.logic.models import User 
from backend.logic.schemas.users import CreateUser, UpdateUser


def create_user(*, session: Session, user_create: CreateUser) -> User:
    """
    Create a new User in the database.

    Args:
        session (Session): Active SQLModel database session.
        user_create (CreateUser): Pydantic model containing the new user's information.

    Returns:
        User: The newly created User object (with hashed password).
    """
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UpdateUser) -> Any:
    """
    Update an existing User's information in the database.

    Args:
        session (Session): Active SQLModel database session.
        db_user (User): The current User object from the database.
        user_in (UpdateUser): Pydantic model containing the fields to update.

    Returns:
        User: The updated User object.
    """
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    Retrieve a User by their email address.

    Args:
        session (Session): Active SQLModel database session.
        email (str): Email address to search for.

    Returns:
        User | None: The found User object if it exists, otherwise None.
    """
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user
