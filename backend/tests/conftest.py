import pytest
from sqlmodel import Session, delete

from backend.core.db import engine, init_db
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


models = [
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
]


@pytest.fixture(scope="session", autouse=True)
def db():
    with Session(engine) as session:
        init_db(session)
        yield session
        for model in models:
            session.exec(delete(model))
        session.commit()