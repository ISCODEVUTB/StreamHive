from collections.abc import Generator
from typing import Annotated
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from pydantic import ValidationError
from sqlmodel import Session

from backend.core.config import settings
from backend.core import security
from backend.core.db import engine
from backend.api.schemas import TokenPayload
from backend.logic.models import User
from backend.logic.enum import UserTypes, UserStatus


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    """
    Provides an active database session for SQLAlchemy operations.

    Returns:
        Session: An active session to interact with the database.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = session.get(User, uuid.UUID(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.user_status == UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_admin(current_user: CurrentUser) -> User:
    if not current_user.user_type == UserTypes.ADMIN:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_internal_or_admin(current_user: CurrentUser):
    internal: bool = current_user.user_type == UserTypes.ADMIN
    admin: bool = current_user.user_type == UserTypes.INTERNAL

    if not (internal or admin):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user