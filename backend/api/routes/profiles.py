import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select
from sqlalchemy.orm import selectinload

from backend.api.schemas import Message
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
from backend.api.deps import CurrentUser, SessionDep, get_current_active_admin, get_current_user


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
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
    dependencies=[Depends(get_current_user)],
    response_model=ProfilePublic
)
def create_profile(*, session: SessionDep, profile_in: CreateProfile, current_user: CurrentUser) -> Any:
    profile = profiles.get_profile_by_username(session=session, username=profile_in.username)
    if profile:
        raise HTTPException(
            status_code=400,
            detail="The profile with this username already exists in the system.",
        )
    try:
        profile = profiles.create_profile(session=session, profile_create=profile_in, user_id=current_user.user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        ) 
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail='User already with profile'
        )
    return profile


@router.delete(
    "/", 
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
def delete_profile(
    session: SessionDep, 
    current_user: CurrentUser
) -> Message:
    statement = select(Profile).where(Profile.user_id == current_user.user_id)
    db_profile = session.exec(statement).first()
    if not db_profile:
        raise HTTPException(
            status_code=404,
            detail="The profile with this id does not exist in the system",
        )
    
    session.delete(db_profile)
    session.commit()
    return Message(message='Profile deleted successfully')


@router.get("/my-profile", response_model=ProfilePublicEXT)
def read_profile_by_user( 
    session: SessionDep,
    current_user: CurrentUser
) -> Any:
    statement = (
        select(Profile)
        .where(Profile.user_id == current_user.user_id)
        .options(
            selectinload(Profile.rating),
            selectinload(Profile.followers),
            selectinload(Profile.following),
            selectinload(Profile.movie_list)
        )
    )
    result = session.exec(statement).first()

    if not result:
        raise HTTPException(status_code=404, detail="Profile not found")

    return ProfilePublicEXT(
        profile_id=result.profile_id,
        image_rel_path=result.image_rel_path,
        username=result.username,
        description=result.description,
        profile_role= result.profile_role,
        lists_count=len(result.movie_list),
        movies_rated=len(result.rating),
        followers_count=len(result.followers),
        following_count=len(result.following)
    )


@router.patch(
    "/update",
    dependencies=[Depends(get_current_user)],
    response_model=ProfilePublic
)
def update_logged_profile(
    *,
    session: SessionDep,
    profile_in: UpdateLogged,
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
    

@router.get("/{profile_id}", response_model=ProfilePublicEXT)
def read_profile_by_id(
    profile_id: uuid.UUID, 
    session: SessionDep,
) -> Any:
    statement = (
        select(Profile)
        .where(Profile.profile_id == profile_id)
        .options(
            selectinload(Profile.rating),
            selectinload(Profile.followers),
            selectinload(Profile.following),
            selectinload(Profile.movie_list)
        )
    )
    result = session.exec(statement).first()

    if not result:
        raise HTTPException(status_code=404, detail="Profile not found")

    return ProfilePublicEXT(
        profile_id=result.profile_id,
        image_rel_path=result.image_rel_path,
        username=result.username,
        description=result.description,
        profile_role= result.profile_role,
        lists_count=len(result.movie_list),
        movies_rated=len(result.rating),
        followers_count=len(result.followers),
        following_count=len(result.following)
    )


@router.patch(
    "/{profile_id}",
    dependencies=[Depends(get_current_active_admin)],
    response_model=ProfilePublic
)
def update_profile(
    *,
    session: SessionDep,
    profile_in: UpdateProfile,
    profile_id: uuid.UUID
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
        if existing_profile and existing_profile.profile_id != db_profile.profile_id:
            raise HTTPException(
                status_code=409, detail="Profile with this username already exists"
            )

    db_profile = profiles.update_profile(session=session, db_profile=db_profile, profile_in=profile_in)
    return db_profile