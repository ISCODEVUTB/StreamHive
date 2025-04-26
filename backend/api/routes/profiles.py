import uuid
from typing import Any, Annotated

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
from backend.logic.controllers import profiles, profile_controller
from backend.api.deps import SessionDep
from backend.logic.entities.profile import Profile, ProfileRoles

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


@router.get("/{profile_id}", response_model=ProfilePublic)
def read_user_by_id(
    profile_id: uuid.UUID, 
    session: SessionDep, 
    #current_user: CurrentUser
) -> Any:
    profile = session.get(Profile, profile_id)
    return profile


@router.post(
    "/", 
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
