import uuid
from sqlmodel import Field, Relationship, SQLModel
from backend.logic.enum import ProfileRoles


class Profile(SQLModel, table=True):
    """
    Database model representing a user's profile.

    Attributes:
        username (str): Unique username for the profile (max 30 characters).
        description (Optional[str]): Short description or bio (max 255 characters).
        profile_role (ProfileRoles): Role of the profile (e.g., subscriber, admin).
        image_rel_path (Optional[str]): Path to the profile's image.
        user_id (UUID): Foreign key linking to the associated user.
        profile_id (UUID): Primary key identifier, auto-generated UUID.

    Relationships:
        user (User): One-to-one relationship back to the User model.
        movie_list (List[MovieList]): One-to-many relationship with movie lists created by the profile.
        interaction (List[Interaction]): One-to-many relationship with interactions (like, comment) made by the profile.
        rating (List[Rating]): One-to-many relationship with movie ratings by the profile.
        following (List[Follow]): Profiles that this profile is following (custom foreign key: follower_id).
        followers (List[Follow]): Profiles that are following this profile (custom foreign key: following_id).
        author_article (List[AuthorArticle]): Articles authored by this profile.
    """
    username: str = Field(unique=True, index=True, max_length=30)
    description: str | None = Field(default=None, max_length=255)
    profile_role: ProfileRoles = Field(default=ProfileRoles.SUBSCRIBER)
    image_rel_path: str | None = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.user_id", unique=True, nullable=False)

    profile_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    user: "User" = Relationship(back_populates="profile")
    movie_list: list["MovieList"] = Relationship(back_populates="profile")
    reaction: list["Reaction"] = Relationship(back_populates="profile")
    comment: list["Comment"] = Relationship(back_populates="profile")
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
    