from sqlmodel import SQLModel, Session, create_engine, select
from pathlib import Path

from backend.logic.models import (
    User, 
    Profile, 
    Follow, 
    Rating, 
    MovieList, 
    Reaction,
    Comment,
    Article,
    Section,
    Newsletter,
    AuthorArticle
)

from backend.logic.schemas.users import CreateUser
from backend.logic.enum import UserTypes, UserGender
from backend.logic.controllers import profiles, users
from backend.data.data import user_test_lists, profile_list_test


# RUTA ABSOLUTA A LA DB
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "thehive.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
test_engine = create_engine(DATABASE_URL, echo=True)

def init_db(session: Session):
    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == 'alex@gmail.com')
    ).first()
    if not user:
        users_in: list[User] = []
        for user_in in user_test_lists:
            users_in.append(users.create_user(session=session, user_create=user_in))

        for i, profile_in in enumerate(profile_list_test):
            profiles.create_profile(session=session, profile_create=profile_in, user_id=users_in[i].user_id)


def init_db_testing(session: Session):
    SQLModel.metadata.create_all(test_engine)

    user = session.exec(
        select(User).where(User.email == 'alex@gmail.com')
    ).first()
    if not user:
        user_in = CreateUser(
            full_name='Alex',
            email='alex@gmail.com',
            password='password1234',
            user_type=UserTypes.ADMIN,
            birth_date='2005-09-15',
            user_gender=UserGender.MALE
        )
        user = users.create_user(session=session, user_create=user_in)
        