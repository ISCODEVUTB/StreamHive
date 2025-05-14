from datetime import datetime
import uuid


class Article:
    """
    Class used to represent an article in the system.
    """

    def __init__(
        self,
        article_id: uuid.UUID,
        content: str,
        image_rel_url: str
    ):
        """
        Initializes an Article object with all its information.

        :param article_id: ID of the article.
        :type article_id: uuid.UUID
        :param content: The textual content of the article.
        :type content: str
        :param image_rel_url: Location of the image used for the article 
        """
        self.__article_id = article_id
        self.__content = content
        self.__image_rel_url = image_rel_url

    @property
    def article_id(self) -> int:
        """
        Returns the article's ID.
        :return: The unique identifier of the article.
        :rtype: int
        """
        return self.__article_id

    @property
    def content(self) -> str:
        """
        Returns the content of the article.
        :return: The article content.
        :rtype: str
        """
        return self.__content

    @content.setter
    def content(self, value: str):
        """
        Sets the content of the article.
        :param value: The new content.
        :type value: str
        """
        self.__content = value

    @property
    def image_rel_url(self) -> str:
        """
        Returns the relative URL of the image.
        :return: Relative path to the image.
        """
        return self.__image_rel_url

    @image_rel_url.setter
    def image_rel_url(self, value: str):
        """
        Sets the relative URL of the image.
        :param value: New relative path.
        """
        self.__image_rel_url = value

    def to_dict(self):
        return dict(
            article_id=str(self.article_id),
            body=dict(
                content=self.content,
                image_rel_url = self.image_rel_url
            )
        )
    
    def __str__(self):
        return str(self.to_dict())