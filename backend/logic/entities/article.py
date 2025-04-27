from datetime import datetime
import uuid


class Article:
    """
    Class used to represent an article in the system.
    """

    def __init__(
        self,
        user_id: uuid.UUID,
        section_id: int,
        content: str,
        created_at: datetime,
        has_spoiler: bool
    ):
        """
        Initializes an Article object with all its information.

        :param user_id: ID of the user who made the article.
        :type user_id: int
        :param section_id: ID of the section of the article.
        :type section_id: int 
        :param content: The textual content of the article.
        :type content: str
        :param created_at: The date and time when the article was posted.
        :type created_at: date
        :param has_spoiler: Indicates if the article contains spoilers.
        :type has_spoiler: bool
        """
        self.__id = uuid.uuid4()
        self.__user_id = user_id
        self.__section_id = section_id
        self.__content = content 
        self.__created_at = created_at
        self.__has_spoiler = has_spoiler

    @property
    def id(self) -> int:
        """
        Returns the article's ID.
        :return: The unique identifier of the article.
        :rtype: int
        """
        return self.__id

    @property
    def user_id(self) -> uuid.UUID:
        """
        Returns the ID of the user who made the article.
        :return: The user's ID.
        :rtype: uuid
        """
        return self.__user_id

    @user_id.setter
    def user_id(self, value: uuid.UUID):
        """
        Sets the user ID associated with the article.
        :param value: The new user ID.
        :type value: uuid
        """
        self.__user_id = value

    @property
    def section_id(self) -> int:
        """
        Returns the ID of the section the article makes part of.
        :return: The section ID.
        :rtype: int
        """
        return self.__section_id

    @section_id.setter
    def section_id(self, value: int):
        """
        Sets the section ID associated with the article.
        :param value: The new section ID.
        :type value: int
        """
        self.__section_id = value

    @property
    def created_at(self) -> datetime:
        """
        Returns the date and time the article was posted.
        :return: The creation timestamp.
        :rtype: date
        """
        return self.__created_at

    @created_at.setter
    def created_at(self, value: datetime):
        """
        Sets the creation date and time of the article.
        :param value: The new creation timestamp.
        :type value: date
        """
        if not isinstance(value, datetime):
            raise TypeError("created_at must be a date object")
        self.__created_at = value

    @property
    def has_spoiler(self) -> bool:
        """
        Returns whether the comment contains spoilers.
        :return: True if the comment has spoilers, False otherwise.
        :rtype: bool
        """
        return self.__has_spoiler

    @has_spoiler.setter
    def has_spoiler(self, value: bool):
        """
        Sets whether the comment contains spoilers.
        :param value: True if it has spoilers, False otherwise.
        :type value: bool
        """
        self.__has_spoiler = value

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

    def to_dict(self):
        return dict(
            id=str(self.id),
            user_id=str(self.user_id),
            section_id=self.section_id,
            content=self.content,
            created_at=self.created_at.isoformat(),
            has_spoiler=self.has_spoiler
        )
    def __str__(self):
        return str(self.to_dict())