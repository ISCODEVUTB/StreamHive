import uuid
from typing import Any
from sqlmodel import Session, select

from backend.core.security import get_password_hash, verify_password
from backend.logic.models import Profile
from backend.logic.schemas.profiles import CreateProfile, UpdateProfile


def create_profile(*, session: Session, profile_create: CreateProfile, user_id: uuid.UUID) -> Profile:
    db_obj = Profile.model_validate(
        profile_create, update={"user_id": user_id}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_profile(*, session: Session, db_profile: Profile, profile_in: UpdateProfile) -> Any:
    profile_data = profile_in.model_dump(exclude_unset=True)
    extra_data = {}
    db_profile.sqlmodel_update(profile_data, update=extra_data)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile


def get_profile_by_username(*, session: Session, username: str) -> Profile | None:
    statement = select(Profile).where(Profile.username == username)
    session_profile = session.exec(statement).first()
    return session_profile
