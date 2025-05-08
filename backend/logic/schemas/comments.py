import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

from backend.logic.enum import TargetTypes


class BaseComment(SQLModel):
    content: str = Field(max_length=500)
    has_spoilers: bool = Field(default=False)


class CreateComment(BaseComment):
    pass


class CommentPublic(BaseComment):
    comment_id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime


class CommentsPublic(SQLModel):
    target_id: str
    target_type: TargetTypes
    comments: list[CommentPublic]
    count: int


class ProfileComment(SQLModel):
    target_id: str
    target_type: TargetTypes
    comment_id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime


class ProfileComments(SQLModel):
    profile_id: uuid.UUID
    comments: list[ProfileComment]
    count: int
