import uuid
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException, Body
from sqlmodel import func, select

#from backend.core.security import get_password_hash
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
from backend.api.deps import SessionDep


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
#    dependencies=[Depends(get_current_active_superuser)],
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


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, 
    session: SessionDep, 
    #current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    """if user == current_user:
        return user
    if not current_user:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )"""
    return user


@router.post(
    "/", 
#    dependencies=[Depends(get_current_active_superuser)], 
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


@router.patch(
    "/{user_id}",
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
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = users.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = users.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user



@router.post(
    "/{user_id}", 
#    dependencies=[Depends(get_current_active_superuser)]
)
def delete_user(
    session: SessionDep, 
#    current_user: CurrentUser, 
    user_id: uuid.UUID
) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    
    user_in = UpdateUser(
        user_status='deleted'
    )

    db_user = users.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete(
    "/{user_id}", 
#    dependencies=[Depends(get_current_active_superuser)]
)
def delete_user_definitely(
    session: SessionDep, 
#    current_user: CurrentUser, 
    user_id: uuid.UUID
) -> None:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    
    session.delete(db_user)
    session.commit()