from typing import Any

from sqlmodel import Session, select

from backend.logic.models import Section, Newsletter 
from backend.logic.schemas.articles_tags import CreateTag, UpdateTag


def create_section(*, session: Session, section_create: CreateTag) -> Section:
    """
    Create a new Section in the database.

    Args:
        session (Session): Active SQLModel database session.
        section_create (CreateTag): Pydantic model containing the data for the new section.

    Returns:
        Section: The newly created Section object.
   """
    db_obj = Section.model_validate(section_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def create_newsletter(*, session: Session, newsletter_create: CreateTag) -> Newsletter:
    """
    Create a new Newsletter in the database.

    Args:
        session (Session): Active SQLModel database session.
        newsletter_create (CreateTag): Pydantic model containing the data for the new newsletter.

    Returns:
        Newsletter: The newly created Newsletter object.
    """
    db_obj = Newsletter.model_validate(newsletter_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_section(*, session: Session, db_tag: Section, tag_in: UpdateTag) -> Any:
    """
    Update an existing Section in the database.

    Args:
        session (Session): Active SQLModel database session.
        db_tag (Section): The current Section object to update.
        tag_in (UpdateTag): Pydantic model containing the updated data.

    Returns:
        Section: The updated Section object.
    """
    tag_data = tag_in.model_dump(exclude_unset=True)
    extra_data = {}
    db_tag.sqlmodel_update(tag_data, update=extra_data)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


def update_newsletter(*, session: Session, db_tag: Newsletter, tag_in: UpdateTag) -> Any:
    """
    Update an existing Newsletter in the database.

    Args:
        session (Session): Active SQLModel database session.
        db_tag (Newsletter): The current Newsletter object to update.
        tag_in (UpdateTag): Pydantic model containing the updated data.

    Returns:
        Newsletter: The updated Newsletter object.
    """
    tag_data = tag_in.model_dump(exclude_unset=True)
    extra_data = {}
    db_tag.sqlmodel_update(tag_data, update=extra_data)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


def get_section_by_name(*, session: Session, name: str) -> Section | None:
    """
    Retrieve a Section by its name.

    Args:
        session (Session): Active SQLModel database session.
        name (str): The name of the section to search for.

    Returns:
        Section | None: The found Section object if it exists, otherwise None.
    """
    statement = select(Section).where(Section.name == name)
    session_section = session.exec(statement).first()
    return session_section


def get_newsletter_by_name(*, session: Session, name: str) -> Newsletter | None:
    """
    Retrieve a Newsletter by its name.

    Args:
        session (Session): Active SQLModel database session.
        name (str): The name of the newsletter to search for.

    Returns:
        Newsletter | None: The found Newsletter object if it exists, otherwise None.
    """
    statement = select(Newsletter).where(Newsletter.name == name)
    session_newsletter = session.exec(statement).first()
    return session_newsletter

