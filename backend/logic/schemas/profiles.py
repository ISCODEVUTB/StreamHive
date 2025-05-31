import uuid
from sqlmodel import Field, SQLModel

from backend.logic.enum.profile_roles import ProfileRoles


class ProfileBase(SQLModel):
    """
    Base model for profile data containing common fields.

    Attributes:
        username (str): The user's display username (max 20 characters).
        description (Optional[str]): A brief user bio or description (max 255 characters).
        profile_role (ProfileRoles): The role assigned to the profile.
    """
    username: str = Field(max_length=20)
    description: str | None = Field(default=None, max_length=255)
    profile_role: ProfileRoles = ProfileRoles.SUBSCRIBER


class CreateProfile(ProfileBase):
    """
    Model for creating a new user profile.

    Attributes:
        image_rel_path (Optional[str]): Relative path to the user's profile image.
    """
    image_rel_path: str | None = Field(default=None)


class UpdateProfile(ProfileBase):
    """
    Model for updating an existing user profile (admin or system-level updates).

    Attributes:
        username (Optional[str]): Updated username.
        image_rel_path (Optional[str]): Updated relative image path.
    """
    username: str | None = Field(default=None, max_length=20)
    image_rel_path: str | None = None


class UpdateLogged(SQLModel):
    """
    Model for logged-in users to update their own profile information.

    Attributes:
        username (Optional[str]): New username.
        description (Optional[str]): New profile description.
        image_rel_path (Optional[str]): New relative image path.
    """
    username: str | None = Field(default=None, max_length=20)
    description: str | None = Field(default=None, max_length=255)
    image_rel_path: str | None = None


class ProfilePublicEXT(ProfileBase):
    """
    Extended public-facing model for a user's profile.

    Attributes:
        profile_id (uuid.UUID): Unique identifier for the profile.
        movies_rated (int): Number of movies rated by the user.
        followers_count (int): Number of followers the user has.
        following_count (int): Number of users the profile is following.
    """
    profile_id: uuid.UUID
    image_rel_path: str
    movies_rated: int
    followers_count: int
    following_count: int


class ProfilePublic(ProfileBase):
    """
    Minimal public-facing model for a user's profile.

    Attributes:
        profile_id (uuid.UUID): Unique identifier for the profile.
    """
    profile_id: uuid.UUID
    image_rel_path: str


class ProfilesPublic(SQLModel):
    """
    Model representing a list of minimal public profiles.

    Attributes:
        profiles (List[ProfilePublic]): List of public profile data.
        count (int): Total number of profiles.
    """
    profiles: list[ProfilePublic]
    count: int


class ProfilesPublicEXT(SQLModel):
    """
    Model representing a list of extended public profiles.

    Attributes:
        profiles (List[ProfilePublic]): List of extended public profile data.
        count (int): Total number of profiles.
    """
    profiles: list[ProfilePublicEXT]
    count: int