import pytest
from sqlmodel import Session
from uuid import uuid4

from backend.logic.models import Reaction
from backend.logic.enum import TargetTypes
from backend.logic.controllers import comments, profiles, reactions, users
from backend.logic.schemas.comments import CreateComment
from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.users import CreateUser
from backend.tests.utils.utils import random_birth_date, random_email, random_lower_string


def user_and_profile_in(db: Session):  
    user_create = CreateUser(
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        full_name='User Example',
        user_gender="other",
        user_type="external"
    )

    user = users.create_user(session=db, user_create=user_create)

    profile_create = CreateProfile(
        username=random_lower_string()
    )

    profile = profiles.create_profile(session=db, profile_create=profile_create, user_id=user.user_id)

    return user, profile


def test_create_reaction_commment(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    comment_in = CreateComment(content="Master to comment", has_spoilers=False)
    target = comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.MOVIE,
        target_id="MovieID"
    )

    reaction = reactions.create_reaction(
        session=db,
        target_type=TargetTypes.COMMENT,
        target_id=str(target.comment_id),
        profile_id=profile.profile_id
    )

    assert reaction
    assert reaction.target_id == str(target.comment_id)
    assert reaction.profile_id == profile.profile_id
    assert reaction.target_type == TargetTypes.COMMENT


def test_get_reactions_by_target_type(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)
    target_id = random_lower_string()
    
    # Crear dos interacciones con el mismo target
    reactions.create_reaction(
        session=db,
        target_type=TargetTypes.MOVIE,
        target_id=target_id,
        profile_id=profile.profile_id
    )

    reactions.create_reaction(
        session=db,
        target_type=TargetTypes.MOVIE,
        target_id=target_id,
        profile_id=profile2.profile_id
    )

    result: list[Reaction] = reactions.get_reactions_by_target(
        session=db, target_type=TargetTypes.MOVIE, target_id=target_id
    )

    assert result
    for inter in result:
        assert inter.target_type == TargetTypes.MOVIE


def test_get_reactions_of_movies_by_profile(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)
    
    reactions.create_reaction(
        session=db,
        target_type=TargetTypes.MOVIE,
        target_id=random_lower_string(),
        profile_id=profile.profile_id
    )

    reactions.create_reaction(
        session=db,
        target_type=TargetTypes.MOVIE,
        target_id=random_lower_string(),
        profile_id=profile2.profile_id
    )

    result: list[Reaction] = reactions.get_reactions_by_profile(
        session=db, profile_id=profile.profile_id, target_type=TargetTypes.MOVIE
    )

    assert result
    for inter in result:
        assert inter.profile_id == profile.profile_id
        assert inter.target_type == TargetTypes.MOVIE


def test_get_reactions_of_comment_by_profile(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    comment_in = CreateComment(content="Master to comment", has_spoilers=False)
    target = comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.MOVIE,
        target_id="MovieID"
    )

    # Crear dos interacciones con el mismo perfil
    reactions.create_reaction(
        session=db,
        target_type=TargetTypes.COMMENT,
        target_id=str(target.comment_id),
        profile_id=profile.profile_id
    )

    reactions.create_reaction(
        session=db,
        target_type=TargetTypes.MOVIE,
        target_id=str(target.comment_id),
        profile_id=profile.profile_id
    )

    result: list[Reaction] = reactions.get_reactions_by_profile(
        session=db, profile_id=profile.profile_id, target_type=TargetTypes.COMMENT
    )

    assert result
    for inter in result:
        assert inter.profile_id == profile.profile_id
        assert inter.target_type == TargetTypes.COMMENT