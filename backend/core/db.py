from sqlmodel import SQLModel, Session, create_engine, select
from pathlib import Path

from backend.logic.models import (
    User, 
    Profile, 
    Follow, 
    Rating, 
    MovieList, 
    Interaction,
    Article,
    Section,
    Newsletter,
    AuthorArticle
)

from backend.logic.schemas.users import CreateUser
from backend.logic.enum import UserTypes
from backend.logic.controllers import users


# RUTA ABSOLUTA A LA DB
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "thehive.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=True)

def init_db(session: Session):
    SQLModel.metadata.create_all(engine)

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
            gender='Masculin'
        )
        user = users.create_user(session=session, user_create=user_in)
        