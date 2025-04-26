import pytest
from sqlmodel import Session, delete

from backend.core.db import engine, init_db
from backend.logic.models import __all__


@pytest.fixture(scope="session", autouse=True)
def db():
    with Session(engine) as session:
        init_db(session)
        yield session
        for model in __all__:
            session.exec(delete(model))
            session.commit()