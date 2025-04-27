from sqlmodel import SQLModel, Field


class CreateTag(SQLModel):
    name: str = Field(max_length=20)


class UpdateTag(SQLModel):
    name: str | None = Field(max_length=20)


class SectionPublic(SQLModel):
    section_id: int
    name: str


class SectionsPublic(SQLModel):
    sections: list[SectionPublic]
    count: int


class NewsletterPublic(SQLModel):
    newsletter_id: int
    name: str


class NewslettersPublic(SQLModel):
    newsletters: list[SectionPublic]
    count: int