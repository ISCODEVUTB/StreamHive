from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from backend.core.db import engine


def get_db():
    """
    Proporciona una sesión de base de datos activa para operaciones SQLAlchemy.

    Returns:
        Session: Una sesión activa para interactuar con la base de datos.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
