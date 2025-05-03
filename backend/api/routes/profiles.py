import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

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
from backend.logic.controllers import profiles
from backend.api.deps import CurrentUser, SessionDep


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get(
    "/",
    response_model=ProfilesPublic,
)
def read_profiles(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(Profile)
    count = session.exec(count_statement).one()

    statement = select(Profile).offset(skip).limit(limit)
    profiles = session.exec(statement).all()

    return ProfilesPublic(profiles=profiles, count=count)


@router.post(
    "/",
    response_model=ProfilePublic
)
def create_profile(*, session: SessionDep, profile_in: CreateProfile, current_user: CurrentUser) -> Any:
    profile = profiles.get_profile_by_username(session=session, username=profile_in.username)
    if profile:
        raise HTTPException(
            status_code=400,
            detail="The profile with this username already exists in the system.",
        )
    
    profile = profiles.create_profile(session=session, profile_create=profile_in, user_id=current_user.user_id)
    return profile


@router.get("/my-profile", response_model=ProfilePublic)
def read_profile_by_user( 
    session: SessionDep,
    current_user: CurrentUser
) -> Any:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    profile = session.exec(statement).first()
    print(profile)
    return profile


@router.patch(
    "/update",
    response_model=ProfilePublic,
)
def update_profile(
    *,
    session: SessionDep,
    profile_in: UpdateProfile,
    current_user: CurrentUser
) -> Any:
    """
    Update a user.
    """
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    db_profile = session.exec(statement).first()
    if not db_profile:
        raise HTTPException(
            status_code=404,
            detail="The profile with this id does not exist in the system",
        )
    if profile_in.username:
        existing_profile = profiles.get_profile_by_username(session=session, username=profile_in.username)
        if existing_profile and existing_profile.profile_id != db_profile.profile_id:
            raise HTTPException(
                status_code=409, detail="Profile with this username already exists"
            )

    db_profile = profiles.update_profile(session=session, db_profile=db_profile, profile_in=profile_in)
    return db_profile


@router.get("/{profile_id}", response_model=ProfilePublic)
def read_profile_by_id(
    profile_id: uuid.UUID, 
    session: SessionDep,
) -> Any:
    profile = session.get(Profile, profile_id)
    return profile


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