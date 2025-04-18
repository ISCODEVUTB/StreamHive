from datetime import datetime, timezone
import uuid
from backend.logic.entities.profile_roles import ProfileRoles


class Profile:
    """
    Class used to represent a profile in the system.
    """

    MAX_USERNAME_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 500
    
    def __init__(
            self,
            username: str,
            description: str,
            profile_pic_url: str,
            profile_role: ProfileRoles,
    ):
        """
        Initializes a Profile object with all its information.

        :param username: The user's display name.
        :type username: str
        :param description: A short bio or description provided by the user.
        :type description: str
        :param profile_pic_url: URL to the user's profile picture.
        :type profile_pic_url: str
        :param profile_role: The role assigned to the user (e.g., subscriber, critic, editor).
        :type profile_role: ProfileRoles
        """
    
        self.__profile_id = str(uuid.uuid4())
        self.__created_at = datetime.now(timezone.utc).isoformat()
        self.username = username
        self.description = description
        self.profile_pic_url = profile_pic_url
        self.profile_role = profile_role
        self.__movie_lists_count = 2
        self.__follower_count = 0
        self.__follow_count = 0
        self.__movies_rated_count = 0
        self.__comments_count = 0

    @property
    def profile_id(self) -> str:
        """
        Returns the profile's id.
        :return: The profile's id.
        :rtype: str
        """
        return self.__profile_id

    @property
    def created_at(self) -> str:
        """
        Returns the profile's creation date.
        :return: The timestamp when the profile was created.
        :rtype: str
        """
        return self.__created_at

    @property
    def username(self) -> str:
        """
        Returns the profile's user name.
        :return: The user name.
        :rtype: str
        """
        return self.__username

    @username.setter
    def username(self, username: str):
        """
        Sets the profile's username.
        :param username: The new username.
        :type username: str
        """
        if len(username) > self.MAX_USERNAME_LENGTH:
            raise ValueError(f"The username cannot exceed {self.MAX_USERNAME_LENGTH} characters.")
        self.__username = username

    @property
    def description(self) -> str:
        """
        Returns the profile's description
        :return: The description.
        :rtype: str
        """
        return self.__description

    @description.setter
    def description(self, description: str):
        """
        Sets the profile's description withe length validation.
        :param description: The new description.
        :type description: str
        """
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"The description cannot exceed {self.MAX_DESCRIPTION_LENGTH} characters.")
        self.__description = description

    @property
    def profile_pic_url(self) -> str:
        """
        Returns the profile's picture url.
        :return: The picture url.
        :rtype: str
        """
        return self.__profile_pic_url

    @profile_pic_url.setter
    def profile_pic_url(self, profile_pic_url: str):
        """
        Sets the profile's picture url.
        :param profile_pic_url: The new picture url.
        :type profile_pic_url: str
        """
        self.__profile_pic_url = profile_pic_url

    @property
    def profile_role(self) -> ProfileRoles:
        """
        Returns the profile's role.
        :return: The type of role.
        :rtype: ProfileRoles
        """
        return self.__profile_role

    @profile_role.setter
    def profile_role(self, role: ProfileRoles):
        """
        Sets the profile's role.
        :param profile_role: The new role.
        :type profile_role: str
        """
        self.__profile_role = role

    @property
    def movie_lists_count(self) -> int:
        """
        Returns the profile's movie lists count.
        :return: The movie list count.
        :rtype: int
        """
        return self.__movie_lists_count

    def increment_movie_lists_count(self):
        """
        Increments the movie lists created by the profile.
        """
        self.__movie_lists_count += 1

    @property
    def follower_count(self) -> int:
        """
        Returns the profile's follower count.
        :return: The follower count.
        :rtype: int
        """
        return self.__follower_count

    def increment_follower_count(self):
        """
        Increments the number of followers
        """
        self.__follower_count += 1

    @property
    def follow_count(self) -> int:
        """
        Returns the profile's follow count.
        :return: The follow count.
        :rtype: int
        """
        return self.__follow_count

    def increment_follow_count(self):
        """
        Increments the number of profiles this profile follows.
        """
        self.__follow_count += 1
    
    @property
    def movies_rated_count(self) -> int:
        """
        Returns the profile's movies rated count.
        :return: The movies rated count.
        :rtype: int
        """
        return self.__movies_rated_count

    def increment_movies_rated_count(self):
        """
        Increments the number of movies the profile has rated.
        """
        self.__movies_rated_count += 1

    @property
    def comments_count(self) -> int:
        """
        Returns the profile's comments count.
        :return: The comments count.
        :rtype: int
        """
        return self.__comments_count

    def increment_comments_count(self):
        """
        Increments the number of comments the profile has made.
        :type increment_comments_count: int
        """
        self.__comments_count += 1

    def __str__(self) -> str:
        """
        Returns a string representation of the Profile object.
        :return: String with profile's basic information.
        :rtype: str
        """
        return dict(
            profile_id=self.profile_id,
            created_at=self.created_at,
            username=self.username,
            description=self.description,
            profile_pic_url=self.profile_pic_url,
            profile_role=self.profile_role.value,
            movie_lists_count=self.movie_lists_count,
            follower_count=self.follower_count,
            follow_count=self.follow_count,
            movies_rated_count=self.movies_rated_count,
            comments_count=self.comments_count
        ).__str__()
