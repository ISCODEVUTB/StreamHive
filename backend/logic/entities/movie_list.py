import uuid


class MovieList:
    """
    Class used to represent a movie list in the system.
    """

    def __init__(
        self,
        id: uuid.UUID,
        profile_id: uuid.UUID
    ):
        """
        Initializes a MovieList object with all necessary attributes.

        :param id: Unique identifier for the movie list.
        :type id: str
        :param profile_id: ID of the user who created the list.
        :type profile_id: int
        :param movies: List of movie IDs included in the list.
        :type movies: list
        """
        self.__id = id
        self.__profile_id = profile_id
        self.__movies = []

    @property
    def id(self) -> uuid.UUID:
        """
        Returns the list's ID.
        :return: The unique identifier of the movie list.
        :rtype: int
        """
        return self.__id

    @property
    def profile_id(self) -> uuid.UUID:
        """
        Returns the ID of the profile who created the list.
        :return: The profile ID.
        :rtype: int
        """
        return self.__profile_id

    @property
    def movies(self) -> list:
        """
        Returns the list of movies in the movie list.
        :return: A list of movie IDs.
        :rtype: list
        """
        return self.__movies

    def to_dict(self):
        """
        Creates a dictionary of all the information
        """
        return dict(            
            id=self.id,
            profile_id=self.profile_id,
            movies= self.movies)

    def __str__(self):
        """
        Returns a string representation of the Movie List object.
        :return: String with the movie list's basic information.
        :rtype: str
        """
        return str(self.to_dict())
