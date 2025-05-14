from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from backend.logic.models import (
    Section,
    Newsletter
)
from backend.logic.schemas.articles_tags import (
    CreateTag,
    UpdateTag,
    SectionPublic,
    SectionsPublic,
    NewsletterPublic,
    NewslettersPublic
)
from backend.logic.controllers import article_tags
from backend.api.deps import SessionDep, get_current_active_internal_or_admin
from backend.api.schemas import Message


router = APIRouter(prefix="/articles/t", tags=["article"])
msg_s = "The section with this id does not exist in the system"
msg_n = "The newsletter with this id does not exist in the system"

@router.get(
    "/sections",
    response_model=SectionsPublic
)
def read_sections(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(Section)
    count = session.exec(count_statement).one()

    statement = select(Section).offset(skip).limit(limit)
    sections= session.exec(statement).all()

    return SectionsPublic(sections=sections, count=count)

@router.get(
    "/newsletters", 
    response_model=NewslettersPublic
)
def read_newsletters(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(Newsletter)
    count = session.exec(count_statement).one()

    statement = select(Newsletter).offset(skip).limit(limit)
    newsletters= session.exec(statement).all()

    return NewslettersPublic(newsletters=newsletters, count=count)


@router.post(
    "/sections", 
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=CreateTag
)
def create_section(*, session: SessionDep, section_in: CreateTag) -> Any:
    section = session.exec(
        select(Section)
        .where(Section.name == section_in.name)
    ).first()
    if section:
        raise HTTPException(
            status_code=400,
            detail=msg_s,
        )
    section = article_tags.create_section(session=session, section_create=section_in)
    return section


@router.post(
    "/newsletters", 
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=CreateTag
)
def create_newsletter(*, session: SessionDep, newsletter_in: CreateTag) -> Any:
    newsletter = session.exec(
        select(Newsletter)
        .where(Newsletter.name == newsletter_in.name)
    ).first()    
    if newsletter:
        raise HTTPException(
            status_code=400,
            detail=msg_s,
        )
    newsletter = article_tags.create_newsletter(session=session, newsletter_create=newsletter_in)
    return newsletter


@router.patch(
    "/sections/{section_id}",
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=SectionPublic
)
def update_section(
    *, session: SessionDep, section_id: int, section_in: UpdateTag,
) -> Any:
    
    db_section = session.get(Section, section_id)
    if not db_section:
        raise HTTPException(
            status_code=404,
            detail=msg_s,
        )

    db_section = article_tags.update_section(session=session, db_tag=db_section, tag_in=section_in)
    return db_section


@router.patch(
    "/newsletters/{newsletter_id}",
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=NewsletterPublic
)
def update_newsletter(
    *, session: SessionDep, newsletter_id: int, newsletter_in: UpdateTag,
) -> Any:
    
    db_newsletter = session.get(Newsletter, newsletter_id)
    if not db_newsletter:
        raise HTTPException(
            status_code=404,
            detail=msg_n,
        )

    db_newsletter = article_tags.update_newsletter(session=session, db_tag=db_newsletter, tag_in=newsletter_in)
    return db_newsletter


@router.delete(
    "/sections/{section_id}", 
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=Message
)
def delete_section(*, session: SessionDep, section_id: int) -> Any:
    db_section = session.get(Section, section_id)
    if not db_section:
        raise HTTPException(
            status_code=404,
            detail=msg_s,
        )
    
    session.delete(db_section)
    session.commit()
    return Message(message='Section deleted successfully')


@router.delete(
    "/newsletters/{newsletter_id}", 
    dependencies=[Depends(get_current_active_internal_or_admin)],
    response_model=Message
)
def delete_newsletter(*, session: SessionDep, newsletter_id: int) -> Any:
    db_newsletter = session.get(Newsletter, newsletter_id)
    if not db_newsletter:
        raise HTTPException(
            status_code=404,
            detail=msg_s,
        )
    
    session.delete(db_newsletter)
    session.commit()
    return Message(message='Newsletter deleted successfully')