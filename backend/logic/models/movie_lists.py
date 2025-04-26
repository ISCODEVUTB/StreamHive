import uuid
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel


class MovieList(SQLModel, table=True):
    name: str = Field(max_length=155)
    description: str | None = Field(max_length=255)
    privacy: bool = False
    profile_id: uuid.UUID = Field(foreign_key="profile.profile_id")

    list_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = datetime.now(timezone.utc)

    profile: "Profile" = Relationship(back_populates="movie_list")
