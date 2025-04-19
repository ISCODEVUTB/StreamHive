from datetime import datetime, timezone
import uuid
from backend.logic.entities.user_status import UserStatus
from backend.logic.entities.user_types import UserTypes
from backend.core.security import get_password_hash


class User:
    """
    Class used to represent a user in the system.
    """

    def __init__(
            self,
            first_name: str,
            last_name: str,
            gender: str,
            birth_date: str,
            email: str,
            phone: str,
            password: str,
            user_type: UserTypes
    ):
        """
        Initializes a User object with all user information.

        :param email: The user's registered email address.
        :type email: str
        :param first_name: The user's first name.
        :type first_name: str
        :param last_name: The user's last name.
        :type last_name: str
        :param phone: The user's phone number.
        :type phone: str
        :param birth_date: The user's date of birth in format YYYY-MM-DD.
        :type birth_date: str
        :param gender: The user's gender.
        :type gender: str
        :param password: The user's password.
        :type password: str
        :param status: The user's status in the app.
        :type status: UserStatus
        :param user_type: The user's type in the app.
        :type password: UserType
        """
        self.__id = str(uuid.uuid4())
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone = phone
        self.__birth_date = birth_date
        self.__gender = gender
        self.__password = get_password_hash(password)
        self.__created_at = str(datetime.now(timezone.utc).isoformat())
        self.__status = UserStatus.ACTIVE
        self.__user_type = user_type

    @property
    def id(self) -> int:
        """Returns the user's id.
        :return: The user's id.
        :rtype: int
        """
        return self.__id

    @property
    def email(self) -> str:
        """Returns the user's email address.
        :return: The email address.
        :rtype: str
        """
        return self.__email

    @email.setter
    def email(self, email: str):
        """Sets the user's email address.
        :param email: The new email address.
        :type email: str
        """
        self.__email = email

    @property
    def first_name(self) -> str:
        """Returns the user's first name.
        :return: The first name.
        :rtype: str
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: str):
        """Sets the user's first name.
        :param first_name: The new first name.
        :type first_name: str
        """
        self.__first_name = first_name

    @property
    def last_name(self) -> str:
        """Returns the user's last name.
        :return: The last name.
        :rtype: str
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: str):
        """Sets the user's last name.
        :param last_name: The new last name.
        :type last_name: str
        """
        self.__last_name = last_name

    @property
    def phone(self) -> str:
        """Returns the user's phone number.
        :return: The phone number.
        :rtype: str
        """
        return self.__phone

    @phone.setter
    def phone(self, phone: str):
        """Sets the user's phone number.
        :param phone: The new phone number.
        :type phone: str
        """
        self.__phone = phone

    @property
    def birth_date(self) -> str:
        """Returns the user's date of birth.
        :return: The birthdate.
        :rtype: str
        """
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, birth_date: str):
        """Sets the user's date of birth.
        :param birth_date: The new birth date.
        :type birth_date: str
        """
        self.__birth_date = birth_date

    @property
    def gender(self) -> str:
        """Returns the user's gender.
        :return: The gender.
        :rtype: str
        """
        return self.__gender

    @gender.setter
    def gender(self, gender: str):
        """Sets the user's gender.
        :param gender: The new gender.
        :type gender: str
        """
        self.__gender = gender

    @property
    def password(self) -> str:
        """Returns the user's password.
        :return: The password.
        :rtype: str
        """
        return self.__password

    @password.setter
    def password(self, password: str):
        """Sets the user's password.
        :param password: The new password.
        :type password: str
        """
        self.__password = get_password_hash(password)

    @property
    def created_at(self) -> str:
        """Returns the user's creation date.
        :return: The timestamp when the user was created.
        :rtype: str
        """
        return self.__created_at

    @property
    def status(self) -> UserStatus:
        """Returns the user's status.
        :return: The user's current status.
        :rtype: UserStatus
        """
        return self.__status

    @status.setter
    def status(self, status: UserStatus):
        """Sets the user's status.
        :param status: The new status.
        :type status: UserStatus
        """
        self.__status = status

    @property
    def user_type(self) -> UserTypes:
        """Returns the user's type.
        :return: The type of user.
        :rtype: UserTypes
        """
        return self.__user_type

    @user_type.setter
    def user_type(self, user_type: UserTypes):
        """Sets the user's type.
        :param type: The new type.
        :type type: UserTypes
        """
        self.__user_type = user_type

    def to_dict(self):
        return dict(
            user_id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            gender=self.gender,
            birth_date=self.birth_date,
            email=self.email,
            phone=self.phone,
            password=self.password,
            created_at=self.created_at,
            user_status=self.status.value,
            user_type=self.user_type.value
        )
    def __str__(self):
        return str(self.to_dict())