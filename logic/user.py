class User:
    """
    Class used to represent a user in the system.
    """

    def init(self, id: int, username: str, email: str, first_name: str, last_name: str, phone: str, birth_date: str, gender: str, password: str):
        """
        Initializes a User object with all user information.

        :param id: A unique number that identifies the user in the system.
        :type id: int
        :param username: The user's chosen username.
        :type username: str
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
        """
        self.__id = id
        self.__username = username
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone = phone
        self.__birth_date = birth_date
        self.__gender = gender
        self.__password = password

    @property
    def id(self) -> int:
        """Returns the user's id.
        :return: The user's id.
        :rtype: int
        """
        return self.__id

    @id.setter
    def id(self, val: int):
        """Sets the user's id.
        :param val: The new id.
        :type val: int
        """
        self.__id = val

    @property
    def username(self) -> str:
        """Returns the user's username.
        :return: The username.
        :rtype: str
        """
        return self.__username

    @username.setter
    def username(self, username: str):
        """Sets the user's username.
        :param username: The new username.
        :type username: str
        """
        self.__username = username

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
        """Returns the user's date of birthdate.
        :return: The birthdate.
        :rtype: str
        """
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, birth_date: str):
        """Sets the user's date of birth.
        :param birth_date: The new birthdate.
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
        self.__password = password

    def _str_(self) -> str:
        """Returns a string representation of the User object.
        :return: String with user's basic information.
        :rtype: str
        """
        return (f"User(id={self._id}, username='{self._username}', "
                f"email='{self._email}', name='{self.first_name} {self._last_name}', "
                f"phone='{self._phone}', birth_date='{self.birth_date}', gender='{self._gender}')")