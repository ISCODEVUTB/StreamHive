from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend.logic.controllers import users
from backend.api.deps import CurrentUser, SessionDep
from backend.core import security
from backend.core.security import get_password_hash
from backend.api.schemas import Token
from backend.logic.schemas.users import UserPublic


router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = users.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.user_status == 'active':
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=60 * 24 * 8)
    return Token(
        access_token=security.create_access_token(
            user.user_id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
