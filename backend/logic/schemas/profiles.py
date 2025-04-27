import uuid
from sqlmodel import Field, SQLModel

from backend.logic.enum.profile_roles import ProfileRoles


class ProfileBase(SQLModel):
    username: str = Field(max_length=20)
    description: str | None = Field(default=None, max_length=255)
    profile_role: ProfileRoles = None


class CreateProfile(ProfileBase):
    image_rel_path: str | None = Field(default=None)


class UpdateProfile(ProfileBase):
    username: str | None = Field(default=None, max_length=20)
    image_rel_path: str | None = None


class UpdateLogged(SQLModel):
    username: str | None = Field(default=None, max_length=20)
    description: str | None = Field(default=None, max_length=255)
    image_rel_path: str | None = None


class ProfilePublicEXT(ProfileBase):
    profile_id: uuid.UUID
    movies_rated: int
    followers_count: int
    following_count: int


class ProfilePublic(ProfileBase):
    profile_id: uuid.UUID


class ProfilesPublic(SQLModel):
    profiles: list[ProfilePublic]
    count: int


class ProfilesPublicEXT(SQLModel):
    profiles: list[ProfilePublicEXT]
    count: int