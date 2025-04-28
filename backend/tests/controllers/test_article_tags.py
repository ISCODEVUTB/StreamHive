from fastapi.encoders import jsonable_encoder
import pytest
from sqlmodel import Session

from backend.logic.models import Section, Newsletter
from backend.logic.controllers import article_tags
from backend.logic.schemas.articles_tags import CreateTag, UpdateTag
from backend.tests.utils.utils import random_lower_string, random_birth_date


def test_create_section(db: Session) -> None:    
    section_in = CreateTag(
        name=random_lower_string(),
        description=random_lower_string()
    )
    section = article_tags.create_section(session=db, section_create=section_in)

    assert section.section_id is not None
    assert section.name == section_in.name


def test_create_newsletter(db: Session) -> None:    
    newsletter_in = CreateTag(
        name=str(random_birth_date()),
        description=random_lower_string()
    )
    newsletter = article_tags.create_newsletter(session=db, newsletter_create=newsletter_in)

    assert newsletter.newsletter_id is not None
    assert newsletter.name == newsletter_in.name


def test_get_section(db: Session) -> None:
    section_in = CreateTag(
        name=random_lower_string(),
        description=random_lower_string()
    )
    section = article_tags.create_section(session=db, section_create=section_in)
    section_2 = db.get(Section, section.section_id)
    
    assert section_2
    assert jsonable_encoder(section) == jsonable_encoder(section_2)


def test_get_newsletter(db: Session) -> None:
    newsletter_in = CreateTag(
        name=str(random_birth_date()),
        description=random_lower_string(),
    )
    newsletter = article_tags.create_newsletter(session=db, newsletter_create=newsletter_in)
    newsletter_2 = db.get(Newsletter, newsletter.newsletter_id)
    
    assert newsletter_2
    assert jsonable_encoder(newsletter) == jsonable_encoder(newsletter_2)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_section(db: Session) -> None:
    section_in = CreateTag(
        name=random_lower_string(),
        description=random_lower_string()
    )
    section = article_tags.create_section(session=db, section_create=section_in)
    
    new_name = random_lower_string()
    section_in_update = UpdateTag(
        name=new_name
    )
    if section.section_id is not None:
        article_tags.update_section(session=db, db_tag=section, tag_in=section_in_update)
    section_2 = db.get(Section, section.section_id)

    assert section_2
    assert section_2.name == new_name


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_update_newsletter(db: Session) -> None:
    newsletter_in = CreateTag(
        name=random_lower_string(),
        description=random_lower_string()
    )
    newsletter = article_tags.create_newsletter(session=db, newsletter_create=newsletter_in)
    
    new_name = random_lower_string()
    newsletter_in_update = UpdateTag(
        name=new_name
    )
    if newsletter.newsletter_id is not None:
        article_tags.update_newsletter(session=db, db_tag=newsletter, tag_in=newsletter_in_update)
    newsletter_2 = db.get(Newsletter, newsletter.newsletter_id)

    assert newsletter_2
    assert newsletter_2.name == new_name