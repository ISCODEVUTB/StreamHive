import uuid
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

#from backend.core.security import get_password_hash
from backend.logic.models import (
    Profile
)
from backend.logic.schemas.profiles import (
    CreateProfile,
    UpdateLogged,
    UpdateProfile,
    ProfilePublic,
    ProfilesPublic,
    ProfilePublicEXT
)
from backend.logic.controllers import profiles, profile_controller
from backend.api.deps import SessionDep


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get(
    "/",
#    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProfilesPublic,
)
def read_profiles(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(Profile)
    count = session.exec(count_statement).one()

    statement = select(Profile).offset(skip).limit(limit)
    profiles = session.exec(statement).all()

    return ProfilesPublic(profiles=profiles, count=count)


@router.get("/{profile_id}", response_model=ProfilePublic)
def read_profile_by_id(
    profile_id: uuid.UUID, 
    session: SessionDep, 
    #current_user: CurrentUser
) -> Any:
    profile = session.get(Profile, profile_id)
    """if user == current_user:
        return user
    if not current_user:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )"""
    return profile


@router.post(
    "/", 
#    dependencies=[Depends(get_current_active_superuser)], 
    response_model=ProfilePublic
)
def create_profile(*, session: SessionDep, profile_in: CreateProfile, user_in: uuid.UUID) -> Any:
    profile = profiles.get_profile_by_username(session=session, username=profile_in.username)
    if profile:
        raise HTTPException(
            status_code=400,
            detail="The profile with this username already exists in the system.",
        )
    
    profile = profiles.create_profile(session=session, profile_create=profile_in, user_id=user_in)
    return profile

@router.patch(
    "/{profile_id}",
    response_model=ProfilePublic,
)
def update_profile(
    *,
    session: SessionDep,
    profile_id: uuid.UUID,
    profile_in: UpdateProfile,
) -> Any:
    """
    Update a user.
    """
    db_profile = session.get(Profile, profile_id)
    if not db_profile:
        raise HTTPException(
            status_code=404,
            detail="The profile with this id does not exist in the system",
        )
    if profile_in.username:
        existing_profile = profiles.get_profile_by_username(session=session, username=profile_in.username)
        if existing_profile and existing_profile.profile_id != profile_id:
            raise HTTPException(
                status_code=409, detail="Profile with this username already exists"
            )

    db_profile = profiles.update_profile(session=session, db_profile=db_profile, profile_in=profile_in)
    return db_profile


@router.delete(
    "/{profile_id}", 
#    dependencies=[Depends(get_current_active_superuser)]
)
def delete_profile(
    session: SessionDep, 
#    current_user: CurrentUser, 
    profile_id: uuid.UUID
) -> None:
    db_profile = session.get(Profile, profile_id)
    if not db_profile:
        raise HTTPException(
            status_code=404,
            detail="The profile with this id does not exist in the system",
        )
    
    session.delete(db_profile)
    session.commit()