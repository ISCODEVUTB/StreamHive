from collections.abc import Generator
import secrets
from typing import Annotated
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from pydantic import ValidationError
from sqlmodel import Session

from backend.core import security
from backend.core.db import engine
from backend.api.schemas import TokenPayload
from backend.logic.models import User
from backend.logic.enum import UserTypes, UserStatus


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    """
    Proporciona una sesión de base de datos activa para operaciones SQLAlchemy.

    Returns:
        Session: Una sesión activa para interactuar con la base de datos.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
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
    print(f'current: {current_user}')
    if not current_user.user_type == UserTypes.ADMIN:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_internal(current_user: CurrentUser) -> User:
    print(f'current: {current_user}')
    if not current_user.user_type == UserTypes.INTERNAL:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
