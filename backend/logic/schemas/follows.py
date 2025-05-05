import uuid
from sqlmodel import SQLModel

from backend.logic.schemas.profiles import ProfilePublic


class FollowersPublic(ProfilePublic):
    followers: list[ProfilePublic]
    count: int


class FollowingPublic(ProfilePublic):
    following: list[ProfilePublic]
    count: int