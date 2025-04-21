import uuid
from sqlmodel import Field, Relationship, SQLModel
from backend.logic.enum import ProfileRoles


class Profile(SQLModel, table=True):
    username: str = Field(unique=True, index=True, max_length=20)
    description: str | None = Field(default=None, max_length=255)
    profile_role: ProfileRoles = Field(default=ProfileRoles.SUBSCRIBER)
    image_rel_path: str | None = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.user_id")

    profile_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    user: "User" = Relationship(back_populates="profile")
    movie_list: list["MovieList"] = Relationship(back_populates="profile")
    interaction: list["Interaction"] = Relationship(back_populates="profile")
    rating: list["Rating"] = Relationship(back_populates="profile")
    following: list["Follow"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    followers: list["Follow"] = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "[Follow.following_id]"}
    )

    author_article: list["AuthorArticle"] = Relationship(back_populates="profile")