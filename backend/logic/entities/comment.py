class Comment:
    """
    Class used to represent a comment in the system.
    """

    def __init__(
        self,
        id:int,
        user_id: int,
        movie_id: int,
        description: str,
        created_at: str,
        like_by: list,
        has_spoiler: bool
    ):
        """
        Initializes a Comment object with all comment information.

        :param id: Unique identifier for the comment.
        :type id: int
        :param user_id: ID of the user who made the comment.
        :type user_id: int
        :param movie_id: ID of the movie the comment refers to.
        :type movie_id: int
        :param description: The content of the comment.
        :type description: str
        :param created_at: The date and time when the comment was created.
        :type created_at: str
        :param like_by: List of user IDs who liked the comment.
        :type like_by: list
        :param has_spoiler: Indicates if the comment contains spoilers.
        :type has_spoiler: bool
        """
        self.__id = id
        self.__user_id = user_id
        self.__movie_id = movie_id
        self.__description = description
        self.__created_at = created_at
        self.__like_by = like_by
        self.__has_spoiler = has_spoiler

    @property
    def id(self) -> int:
        """
        Returns the comment's ID.
        :return: The unique identifier of the comment.
        :rtype: int
        """
        return self.__id

    @id.setter
    def id(self, value: int):
        """
        Sets the comment's ID.
        :param value: The new ID.
        :type value: int
        """
        self.__id = value

    @property
    def user_id(self) -> int:
        """
        Returns the ID of the user who made the comment.
        :return: The user's ID.
        :rtype: int
        """
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int):
        """
        Sets the user ID associated with the comment.
        :param value: The new user ID.
        :type value: int
        """
        self.__user_id = value

    @property
    def movie_id(self) -> int:
        """
        Returns the ID of the movie the comment is related to.
        :return: The movie ID.
        :rtype: int
        """
        return self.__movie_id

    @movie_id.setter
    def movie_id(self, value: int):
        """
        Sets the movie ID associated with the comment.
        :param value: The new movie ID.
        :type value: int
        """
        self.__movie_id = value

    @property
    def description(self) -> str:
        """
        Returns the description of the comment.
        :return: The text of the comment.
        :rtype: str
        """
        return self.__description

    @description.setter
    def description(self, value: str):
        """
        Sets the comment's description.
        :param value: The new description.
        :type value: str
        """
        self.__description = value

    @property
    def created_at(self) -> str:
        """
        Returns the date and time the comment was created.
        :return: The creation timestamp.
        :rtype: str
        """
        return self.__created_at

    @created_at.setter
    def created_at(self, value: str):
        """
        Sets the creation date and time of the comment.
        :param value: The new creation timestamp.
        :type value: str
        """
        self.__created_at = value

    @property
    def like_by(self) -> list:
        """
        Returns the list of users who liked the comment.
        :return: A list of user IDs or usernames who liked the comment.
        :rtype: list
        """
        return self.__like_by

    @like_by.setter
    def like_by(self, value: list):
        """
        Sets the list of users who liked the comment.
        :param value: The new list of likes.
        :type value: list
        """
        self.__like_by = value

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

    def _str_(self):
        return dict(id=self.id, user_id=self.user_id, movie_id=self.movie_id,
                    description=self.description,created_at=self.created_at,
                    like_by=self.like_by,has_spoiler=self.has_spoiler).__str__()