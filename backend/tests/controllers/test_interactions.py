import pytest
from sqlmodel import Session
from uuid import uuid4

from backend.logic.models import Interaction
from backend.logic.schemas.interactions import CreateInteraction, InteractTypes, TargetTypes
from backend.logic.controllers import interactions, profiles, users
from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.users import CreateUser
from backend.tests.utils.utils import random_birth_date, random_email, random_lower_string


def user_and_profile_in(session: Session):  
    user_create = CreateUser(
        email=random_email(), 
        password =random_lower_string(),
        birth_date=random_birth_date(),
        full_name='User Example',
        user_gender="other",
        user_type="external"
    )

    user = users.create_user(session=session, user_create=user_create)

    profile_create = CreateProfile(
        username=random_lower_string()
    )

    profile = profiles.create_profile(session=session, profile_create=profile_create, user_id=user.user_id)

    return user, profile


def test_create_interaction(db: Session) -> None:
    _, profile = user_and_profile_in(db)

    target_id = uuid4()
    interaction_in = CreateInteraction(
        target_id=target_id,
        target_type=TargetTypes.MOVIE,
        interaction_type=InteractTypes.LIKED,
        profile_id=profile.profile_id
    )

    interaction = interactions.create_interaction(
        session=db, interaction_create=interaction_in
    )

    assert interaction
    assert interaction.target_id == interaction_in.target_id
    assert interaction.profile_id == profile.profile_id
    assert interaction.interaction_type == InteractTypes.LIKED
    assert interaction.target_type == TargetTypes.MOVIE


def test_get_interactions_by_target_type(db: Session) -> None:
    _, profile = user_and_profile_in(db)
    target_id = uuid4()
    
    # Crear dos interacciones con el mismo target
    for _ in range(2):
        print(_, end=" ")
        interaction_in = CreateInteraction(
            target_id=target_id,
            target_type=TargetTypes.MOVIE,
            interaction_type=InteractTypes.LIKED,
            profile_id=profile.profile_id
        )
        interactions.create_interaction(session=db, interaction_create=interaction_in)

    result: list[Interaction] = interactions.get_interactions_by_target(
        session=db, target_type=TargetTypes.MOVIE
    )

    assert result
    for inter in result:
        assert inter.target_type == TargetTypes.MOVIE


def test_get_interactions_by_interaction_type(db: Session) -> None:
    _, profile = user_and_profile_in(db)

    # Crear dos interacciones: una 'liked', otra 'comment'
    interaction_1 = CreateInteraction(
        target_id=uuid4(),
        target_type=TargetTypes.ARTICLE,
        interaction_type=InteractTypes.LIKED,
        profile_id=profile.profile_id
    )
    interaction_2 = CreateInteraction(
        target_id=uuid4(),
        target_type=TargetTypes.ARTICLE,
        interaction_type=InteractTypes.COMMENT,
        profile_id=profile.profile_id
    )

    interactions.create_interaction(session=db, interaction_create=interaction_1)
    interactions.create_interaction(session=db, interaction_create=interaction_2)

    liked_results: list[Interaction] = interactions.get_interactions_by_profile(
        session=db, interaction_type=InteractTypes.LIKED
    )

    assert liked_results
    for inter in liked_results:
        assert inter.interaction_type == InteractTypes.LIKED