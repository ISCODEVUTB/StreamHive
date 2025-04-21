import pytest
from sqlmodel import Session, delete

from backend.core.db import engine, init_db
from backend.logic.models import (
    User,
    Profile
)


@pytest.fixture(scope="session", autouse=True)
def db():
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Profile)
        session.exec(statement)
        statement = delete(User)
        session.exec(statement)
        session.commit()