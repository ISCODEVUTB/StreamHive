from sqlmodel import SQLModel, Field


class CreateTag(SQLModel):
    """
    Model for creating a new tag.

    Attributes:
        name (str): Name of the tag (max 20 characters).
        description (Optional[str]): Optional description of the tag (max 255 characters).
    """
    name: str = Field(max_length=20)
    description: str | None = Field(default=None, max_length=255)


class UpdateTag(SQLModel):
    """
    Model for updating an existing tag.

    Attributes:
        name (Optional[str]): Updated tag name (max 20 characters).
        description (Optional[str]): Updated tag description (max 255 characters).
    """
    name: str | None = Field(default=None, max_length=20)
    description: str | None = Field(default=None, max_length=255)


class SectionPublic(SQLModel):
    """
    Public-facing model for a section.

    Attributes:
        section_id (int): Unique identifier of the section.
        name (str): Name of the section.
    """
    section_id: int
    name: str


class SectionsPublic(SQLModel):
    """
    Model representing a list of public sections.

    Attributes:
        sections (List[SectionPublic]): List of sections.
        count (int): Total number of sections.
    """
    sections: list[SectionPublic]
    count: int


class NewsletterPublic(SQLModel):
    """
    Public-facing model for a newsletter.

    Attributes:
        newsletter_id (int): Unique identifier of the newsletter.
        name (str): Name of the newsletter.
    """
    newsletter_id: int
    name: str


class NewslettersPublic(SQLModel):
    """
    Model representing a list of public newsletters.

    Attributes:
        newsletters (List[SectionPublic]): List of newsletters.
        count (int): Total number of newsletters.
    """
    newsletters: list[SectionPublic]
    count: int