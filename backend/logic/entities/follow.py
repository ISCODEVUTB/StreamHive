from datetime import datetime


class Follow:
    """
    Class used to represent a follow done by a user profile in the system.
    """

    def __init__(
        self,
        follower_id: int,
        following_id: int,
        created_at: datetime
    ):
        """
        Initializes a Follow object.

        :param follower_id: ID of the follower profile.
        :type follower_id: int
        :param following_id: ID of the profile following.
        :type following_id: int                                     
        :param created_at: Timestamp when the following was done.
        :type created_at: datetime
        """
        self.__follower_id = follower_id
        self.__following_id = following_id
        self.created_at = created_at

    @property
    def follower_id(self) -> int:
        """
        Returns the ID of the profile doing the following (follower)
        :return: The follower profile's ID.
        :rtype: int
        """
        return self.__follower_id

    @follower_id.setter
    def follower_id(self, value: int):
        """
        Sets the profile ID doing the following.
        :param value: The new follower's ID.
        :type value: int
        """
        self.__follower_id = value

    @property
    def following_id(self) -> int:
        """
        Returns the ID of the profile being followed
        :return: The following profile's ID.
        :rtype: int
        """
        return self.__following_id

    @following_id.setter
    def following_id(self, value: int):
        """
        Sets the profile following ID.
        :param value: The new following profile's ID.
        :type value: int
        """
        self.__following_id = value

    @property
    def created_at(self) -> datetime:
        """
        Returns the date and time the following was done.
        :return: The creation timestamp.
        :rtype: datetime
        """
        return self.__created_at

    @created_at.setter
    def created_at(self, value: datetime):
        """
        Sets the creation date and time of the following.
        :param value: The new creation timestamp.
        :type value: datetime
        """
        if not isinstance(value, datetime):
            raise TypeError("created_at must be a datetime object")
        self.__created_at = value

    def to_dict(self):
        return dict(            
            follower_id=self.follower_id ,
            following_id=self.following_id,
            created_at= self.created_at)

    def __str__(self):

            return str(self.to_dict())
