import uuid
from sqlmodel import SQLModel, Field, Relationship


class AuthorArticle(SQLModel, table=True):
    profile_id: uuid.UUID = Field(foreign_key='profile.profile_id' ,primary_key=True)
    article_id: uuid.UUID = Field(foreign_key='article.article_id', primary_key=True, ondelete='CASCADE')
    main_author: bool = False

    profile: "Profile" = Relationship(back_populates='author_article')
    article: "Article" = Relationship(back_populates='author_article')