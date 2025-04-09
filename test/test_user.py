import unittest
from logic.user import User


class TestUser(unittest.TestCase):
    """
    Test cases for the User class.

    The TestUser class contains unit tests that verify the behavior and functionality
    of the User class methods, including property getters, setters, and string representation.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a sample User object.
        """
        self.user = User(
            id=12345,
            username="JohnDoe1",
            email="johndoe123@hotmail.com",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            birth_date="1999-05-05",
            gender="Masculin",
            password="password123"
        )

    def test__init_(self):
        """
        Test the initialization of the User object.
    
        Verifies if all attributes of the User object are correctly set during initialization.
        """
        self.assertEqual(self.user.id, 12345, "The ID was not initialized correctly.")
        self.assertEqual(self.user.username, "JohnDoe1", "The username was not initialized correctly.")
        self.assertEqual(self.user.email, "johndoe123@hotmail.com", "The email was not initialized correctly.")
        self.assertEqual(self.user.first_name, "John", "The first name was not initialized correctly.")
        self.assertEqual(self.user.last_name, "Doe", "The last name was not initialized correctly.")
        self.assertEqual(self.user.phone, "1234567890", "The phone number was not initialized correctly.")
        self.assertEqual(self.user.birth_date, "1999-05-05", "The birthdate was not initialized correctly.")
        self.assertEqual(self.user.gender, "Masculin", "The gender was not initialized correctly.")
        self.assertEqual(self.user.password, "password123", "The password was not initialized correctly.")

if __name__ == '__main__':
    unittest.main()
