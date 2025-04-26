from sqlmodel import SQLModel, Field, Relationship


class TagBase(SQLModel):
    name: str = Field(max_length=20)
    description: str | None = Field(max_length=225)

class Section(TagBase, table=True):
    section_id: int | None = Field(default=None, primary_key=True)

    article: "Article" = Relationship(back_populates='section')

class Newsletter(TagBase, table=True):
    newsletter_id: int | None = Field(default=None, primary_key=True)

    article: "Article" = Relationship(back_populates='newsletter')
    