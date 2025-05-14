import pytest
import uuid
from sqlmodel import Session
from backend.logic.controllers import comments
from backend.logic.schemas.comments import CreateComment
from backend.logic.enum import TargetTypes
from backend.tests.utils.user import user_and_profile_in


def test_create_comment(db: Session):
    _, profile = user_and_profile_in(db)
    comment_in = CreateComment(content="This is a movie comment", has_spoilers=False)
    target_id = "tt1234567"

    comment = comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.MOVIE,
        target_id=target_id
    )

    assert comment
    assert comment.content == comment_in.content
    assert comment.target_id == target_id
    assert comment.target_type == TargetTypes.MOVIE
    assert comment.profile_id == profile.profile_id


def test_get_comments_by_target(db: Session):
    _, profile = user_and_profile_in(db)
    comment_in = CreateComment(content="Sample Comment Target", has_spoilers=True)
    target_id = uuid.uuid4()
    target_type = TargetTypes.COMMENT

    comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=target_type,
        target_id=str(target_id),
    )

    result = comments.get_comments_by_target(
        session=db,
        target_type=target_type,
        target_id=target_id
    )

    assert result
    assert any(c.content == comment_in.content for c in result)


def test_get_comments_by_profile(db: Session):
    _, profile = user_and_profile_in(db)
    comment_in = CreateComment(content="Sample Comment Profile", has_spoilers=False)
    target_id = str(uuid.uuid4())

    comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.COMMENT,
        target_id=target_id,
    )

    result = comments.get_comments_by_profile(session=db, profile_id=profile.profile_id)

    assert result
    assert any(c.content == comment_in.content for c in result)


def test_create_comment_on_comment(db: Session):
    _, profile = user_and_profile_in(db)
    comment_in = CreateComment(content="Master to comment", has_spoilers=False)
    parent_comment = comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.MOVIE,
        target_id="MovieID"
    )

    comment_in = CreateComment(content="Reply to comment", has_spoilers=False)
    comment = comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.COMMENT,
        target_id=str(parent_comment.comment_id)
    )

    assert comment
    assert comment.target_id == str(parent_comment.comment_id)
    assert comment.target_type == TargetTypes.COMMENT


def test_get_comments_by_target(db: Session):
    _, profile = user_and_profile_in(db)
    movie_id = "tt6543210"
    comment_in = CreateComment(content="Another comment", has_spoilers=True)

    comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.MOVIE,
        target_id=movie_id
    )

    result = comments.get_comments_by_target(
        session=db,
        target_type=TargetTypes.MOVIE,
        target_id=movie_id
    )

    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0].target_id == movie_id


def test_get_comments_by_profile(db: Session):
    _, profile = user_and_profile_in(db)
    movie_id = "tt1111111"
    comment_in = CreateComment(content="Profile comment", has_spoilers=False)

    comments.create_comment(
        session=db,
        comment_in=comment_in,
        profile_id=profile.profile_id,
        target_type=TargetTypes.MOVIE,
        target_id=movie_id
    )

    result = comments.get_comments_by_profile(
        session=db,
        profile_id=profile.profile_id
    )

    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0].profile_id == profile.profile_id


def test_get_comments_not_found(db: Session):
    fake_uuid = uuid.uuid4()
    result_by_profile = comments.get_comments_by_profile(
        session=db,
        profile_id=fake_uuid
    )
    assert result_by_profile == []

    result_by_target = comments.get_comments_by_target(
        session=db,
        target_type=TargetTypes.COMMENT,
        target_id=str(uuid.uuid4())
    )
    assert result_by_target == []