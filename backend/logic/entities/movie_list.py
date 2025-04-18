import uuid


class MovieList:
    """
    Class used to represent a movie list in the system.
    """

    MAX_LIST_NAME_LENGTH = 200
    MAX_LIST_DESCRIPTION_LENGTH = 1000

    def __init__(
        self,
        id: str,
        user_id: int,
        privacy: str,
        list_name: str,
        list_description: str,
        like_by: list,
        saved_by: list,
        movies: list
    ):
        """
        Initializes a MovieList object with all necessary attributes.

        :param id: Unique identifier for the movie list.
        :type id: int
        :param user_id: ID of the user who created the list.
        :type user_id: int
        :param privacy: Privacy setting of the list (e.g., 'public', 'private').
        :type privacy: str
        :param list_name: The name of the movie list.
        :type list_name: str
        :param list_description: Description of the movie list.
        :type list_description: str
        :param like_by: List of user IDs who liked the list.
        :type like_by: list
        :param saved_by: List of user IDs who saved the list.
        :type saved_by: list
        :param movies: List of movie IDs included in the list.
        :type movies: list
        """
        self.__id = id if id else str(uuid.uuid4())
        self.__user_id = user_id
        self.privacy = privacy
        self.list_name = list_name
        self.list_description = list_description
        self.__like_by = like_by if like_by is not None else []
        self.__saved_by = saved_by if saved_by is not None else []
        self.__movies = movies if movies is not None else []

    @property
    def id(self) -> str:
        """
        Returns the list's ID.
        :return: The unique identifier of the movie list.
        :rtype: int
        """
        return self.__id

    @property
    def user_id(self) -> int:
        """
        Returns the ID of the user who created the list.
        :return: The user ID.
        :rtype: int
        """
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int):
        """
        Sets the user ID of the list creator.
        :param value: The new user ID.
        :type value: int
        """
        self.__user_id = value

    @property
    def privacy(self) -> str:
        """
        Returns the privacy setting of the list.
        :return: The privacy value (e.g., 'public', 'private').
        :rtype: str
        """
        return self.__privacy

    @privacy.setter
    def privacy(self, value: str):
        """
        Sets the privacy setting of the list.
        :param value: The new privacy setting.
        :type value: str
        """
        if value not in ["public", "private"]:
            raise ValueError("Privacy must be either 'public' or 'private'.")
        self.__privacy = value

    @property
    def list_name(self) -> str:
        """
        Returns the name of the movie list.
        :return: The name of the list.
        :rtype: str
        """
        return self.__list_name

    @list_name.setter
    def list_name(self, value: str):
        """
        Sets the name of the movie list.
        :param value: The new list name.
        :type value: str
        """
        if len(value) > self.MAX_LIST_NAME_LENGTH:
            raise ValueError(f"The list name cannot exceed {self.MAX_LIST_NAME_LENGTH} characters.")
        self.__list_name = value

    @property
    def list_description(self) -> str:
        """
        Returns the description of the movie list.
        :return: The list description.
        :rtype: str
        """
        return self.__list_description

    @list_description.setter
    def list_description(self, value: str):
        """
        Sets the description of the movie list.
        :param value: The new description.
        :type value: str
        """
        if len(value) > self.MAX_LIST_DESCRIPTION_LENGTH:
            raise ValueError(f"The list description cannot exceed {self.MAX_LIST_DESCRIPTION_LENGTH} characters.")
        self.__list_description = value

    @property
    def like_by(self) -> list:
        """
        Returns the list of users who liked the movie list.
        :return: A list of user IDs.
        :rtype: list
        """
        return self.__like_by

    @like_by.setter
    def like_by(self, value: list):
        """
        Sets the list of users who liked the movie list.
        :param value: The new list of likes.
        :type value: list
        """
        self.__like_by = value

    @property
    def saved_by(self) -> list:
        """
        Returns the list of users who saved the movie list.
        :return: A list of user IDs.
        :rtype: list
        """
        return self.__saved_by

    @saved_by.setter
    def saved_by(self, value: list):
        """
        Sets the list of users who saved the movie list.
        :param value: The new list of saves.
        :type value: list
        """
        self.__saved_by = value

    @property
    def movies(self) -> list:
        """
        Returns the list of movies in the movie list.
        :return: A list of movie IDs.
        :rtype: list
        """
        return self.__movies

    @movies.setter
    def movies(self, value: list):
        """
        Sets the list of movies in the movie list.
        :param value: The new list of movie IDs.
        :type value: list
        """
        self.__movies = value

    def to_dict(self):
        """
        Creates a dictionary of all the information
        """
        return dict(            
            id=self.id,
            user_id= self.user_id,
            privacy= self.privacy,
            list_name= self.list_name,
            list_description= self.list_description,
            like_by=self.like_by,
            saved_by= self.saved_by,
            movies= self.movies)

    def __str__(self):
        return str(self.to_dict())
