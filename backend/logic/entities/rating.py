#  profile id, movie id, rate decimal, created at time stamp
from datetime import datetime


class Rating:
    """
    Class used to represent a movie rating given by a user profile in the system.
    """

    def __init__(
        self,
        profile_id: int,
        movie_id: int,
        rate: float,
        created_at: datetime
    ):
        """
        Initializes a Rate object.

        :param profile_id: ID of the profile giving the rating.
        :type profile_id: int
        :param movie_id: ID of the movie being rated.
        :type movie_id: int
        :param rate: The rating given to the movie (e.g., 4.5).
        :type rate: float
        :param created_at: Timestamp when the rating was created.
        :type created_at: datetime
        """
        self.__profile_id = profile_id
        self.__movie_id = movie_id
        self.rate = rate
        self.created_at = created_at

    @property
    def profile_id(self) -> int:
        """
        Returns the ID of the profile who made the rating.
        :return: The user's ID.
        :rtype: int
        """
        return self.__profile_id

    @profile_id.setter
    def profile_id(self, value: int):
        """
        Sets the profile ID associated with the comment.
        :param value: The new user ID.
        :type value: int
        """
        self.__profile_id = value

    @property
    def movie_id(self) -> int:
        """
        Returns the ID of the movie the rating is related to.
        :return: The movie ID.
        :rtype: int
        """
        return self.__movie_id

    @movie_id.setter
    def movie_id(self, value: int):
        """
        Sets the movie ID associated with the rating.
        :param value: The new movie ID.
        :type value: int
        """
        self.__movie_id = value

    @property
    def rate(self) -> float:
        """
        Returns the rating of the movie.
        :return: Rating.
        :rtype: float
        """
        return self.__rate

    @rate.setter
    def rate(self, value: float):
        """
        Sets the rating of the movie.
        :param value: The new rating.
        :type value: float
        """
        if not (0 <= value <= 5):
            raise ValueError("rate must be between 0 and 5")
        self.__rate = value

    @property
    def created_at(self) -> datetime:
        """
        Returns the date and time the rating was done.
        :return: The creation timestamp.
        :rtype: datetime
        """
        return self.__created_at

    @created_at.setter
    def created_at(self, value: datetime):
        """
        Sets the creation date and time of the rating.
        :param value: The new creation timestamp.
        :type value: datetime
        """
        if not isinstance(value, datetime):
            raise TypeError("created_at must be a datetime object")
        self.__created_at = value
    
    def to_dict(self):
        return dict(
            profile_id=self.profile_id,
            movie_id= self.movie_id,
            rate=self.rate,
            created_at=self.created_at
        )
    def __str__(self):
        return str(self.to_dict())
