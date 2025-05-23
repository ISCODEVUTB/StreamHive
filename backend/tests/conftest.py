from typing import Generator
from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, delete

from backend.core.db import init_db_testing, test_engine
from backend.core.config import settings
from backend.app import app
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
from backend.tests.utils.user import authentication_token_from_email
from backend.tests.utils.utils import get_superuser_token_headers


models = [ 
    Reaction,
    Comment,
    Rating,
    MovieList,
    Follow,
    AuthorArticle,
    Article,
    Newsletter,
    Section,
    Profile,
    User
]


@pytest.fixture(scope="session")
def db():
    with Session(test_engine) as session:
        init_db_testing(session)
        yield session
        for model in models:
            """if model is User:
                continue"""
            session.exec(delete(model))
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )