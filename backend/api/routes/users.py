from typing import Any, Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.api.schemas import Message
from backend.core.security import verify_password
from backend.logic.models import (
    User
)
from backend.logic.schemas.users import (
    CreateUser,
    UpdateLogged,
    UpdatePassword,
    UpdateUser,
    RegisterUser,
    UserPublic,
    UsersPublic
)
from backend.logic.controllers import users
from backend.api.deps import CurrentUser, SessionDep, get_current_active_admin, get_current_user


router = APIRouter(prefix="/users", tags=["users"])
msg = "The user with this id does not exist in the system"


@router.get(
    "/",
    dependencies=[Depends(get_current_active_admin)],
    response_model=UsersPublic,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """

    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(users=users, count=count)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_admin)],
    response_model=UserPublic
)
def create_user(*, session: SessionDep, user_in: CreateUser) -> Any:
    """
    Create new user.
    """
    user = users.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    user = users.create_user(session=session, user_create=user_in)
    return user


@router.post(
    "/signup",
    response_model=UserPublic
)
def register_user(*, session: SessionDep, user_in: RegisterUser) -> Any:
    """
    Register new user.
    """
    user = users.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    user = users.create_user(session=session, user_create=user_in)
    return user


@router.get(
    "/account",
    response_model=UserPublic
)
def read_user_logged_account(
    session: SessionDep,
    current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, current_user.user_id)
    return user


@router.patch(
    "/account",
    response_model=UserPublic,
)
def update_logged_user(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    user_in: UpdateLogged,
) -> Any:
    """
    Update a user.
    """
    db_user = session.get(User, current_user.user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    if user_in.email:
        existing_user = users.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.user_id != current_user.user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = users.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.patch(
    "/account/password",
    dependencies=[Depends(get_current_user)],
    response_model=Message   
)
def update_password(
    session: SessionDep,
    user_in: UpdatePassword,
    current_user: CurrentUser
) -> Any:
    """
    Update a user's password.
    """
    db_user = session.get(User, current_user.user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    if not verify_password(user_in.current_password, db_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )

    db_user = users.update_user(session=session, db_user=db_user, user_in=user_in)
    return Message(message='Password updated successfully')


@router.post(
    "/account/delete",
    dependencies=[Depends(get_current_user)]
)
def delete_user(
    session: SessionDep, 
    current_user: CurrentUser
) -> User:
    db_user = session.get(User, current_user.user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    
    user_in = UpdateUser(
        email=f"deleted-user-{current_user.user_id}@example.com",
        user_status='deleted'
    )

    db_user = users.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.get(
    "/{user_id}", 
    dependencies=[Depends(get_current_active_admin)],
    response_model=UserPublic
)
def read_user_by_id(
    user_id: uuid.UUID, 
    session: SessionDep
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_admin)],
    response_model=UserPublic,
)
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UpdateUser,
) -> Any:
    """
    Update a user.
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    if user_in.email:
        existing_user = users.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = users.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete(
    "/{user_id}", 
    dependencies=[Depends(get_current_active_admin)],
    response_model=Message
)
def delete_user(
    session: SessionDep,
    user_id: uuid.UUID
) -> Message:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=msg,
        )
    
    session.delete(db_user)
    session.commit()
    return Message(message='User deleted successfully')