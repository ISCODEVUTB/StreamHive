import uuid
from sqlmodel import Session

from backend.logic.models import Follow
from backend.logic.controllers import follows
from backend.tests.utils.user import user_and_profile_in


def test_create_follow(db: Session) -> None:
    _, profile1 = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)

    follow = follows.create_follow(session=db, following_id=profile2.profile_id, follower_id=profile1.profile_id)

    assert follow.follower_id==profile1.profile_id
    assert follow.following_id==profile2.profile_id


def test_get_profile_followers(db: Session) -> None:
    _, profile1 = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)

    db.add(Follow(follower_id=profile1.profile_id, following_id=profile2.profile_id))
    db.commit()

    followers = follows.get_profile_followers(session=db, profile_id=profile2.profile_id)

    assert followers.count == 1
    assert followers.followers[0].profile_id == profile1.profile_id


def test_get_profile_followers_empty(db: Session) -> None:
    _, profile2 = user_and_profile_in(db)

    followers = follows.get_profile_followers(session=db, profile_id=profile2.profile_id)

    assert followers.count == 0
    assert followers.followers == []


def test_get_profile_not_found_followers(db: Session) -> None:
    _, profile1 = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)

    db.add(Follow(follower_id=profile1.profile_id, following_id=profile2.profile_id))
    db.commit()

    nonexistent_profile_id = uuid.uuid4()
    followers = follows.get_profile_followers(session=db, profile_id=nonexistent_profile_id)

    assert followers is None


def test_get_profile_following(db: Session) -> None:
    _, profile1 = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)
    
    db.add(Follow(follower_id=profile1.profile_id, following_id=profile2.profile_id))
    db.commit()

    following = follows.get_profile_following(session=db, profile_id=profile1.profile_id)

    assert following.count == 1
    assert following.following[0].profile_id == profile2.profile_id


def test_get_profile_following_empty(db: Session) -> None:
    _, profile1 = user_and_profile_in(db)

    following = follows.get_profile_following(session=db, profile_id=profile1.profile_id)

    assert following.count == 0
    assert following.following == []


def test_get_profile_not_found_following(db: Session) -> None:
    _, profile1 = user_and_profile_in(db)
    _, profile2 = user_and_profile_in(db)

    db.add(Follow(follower_id=profile1.profile_id, following_id=profile2.profile_id))
    db.commit()

    nonexistent_profile_id = uuid.uuid4()
    following = follows.get_profile_following(session=db, profile_id=nonexistent_profile_id)

    assert following is None