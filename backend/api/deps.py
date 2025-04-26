from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from backend.core.db import engine


def get_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
