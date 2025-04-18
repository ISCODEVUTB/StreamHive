import unittest
from datetime import datetime
from backend.logic.entities.user import User
from backend.logic.entities.user_status import UserStatus
from backend.logic.entities.user_types import UserTypes
from backend.core.security import verify_password


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
        self.raw_password = "Password123"
        self.user = User(
            first_name="John",
            last_name="Doe",
            gender="Masculin",
            birth_date="1999-05-05",
            email="johndoe123@hotmail.com",
            phone="1234567890",
            password=self.raw_password,
            user_type=UserTypes.EXTERNAL
        )

    def test_user(self):
        """
        Test the initialization of the User object.
    
        Verifies if all attributes of the User object are correctly set during initialization.
        """
        self.assertIsNotNone(self.user.id)
        self.assertEqual(self.user.first_name, "John", "The first name was not initialized correctly.")
        self.assertEqual(self.user.last_name, "Doe", "The last name was not initialized correctly.")
        self.assertEqual(self.user.gender, "Masculin", "The gender was not initialized correctly.")
        self.assertEqual(self.user.birth_date, "1999-05-05", "The birthdate was not initialized correctly.")
        self.assertEqual(self.user.email, "johndoe123@hotmail.com", "The email was not initialized correctly.")
        self.assertEqual(self.user.phone, "1234567890", "The phone number was not initialized correctly.")
        self.assertTrue(verify_password(self.raw_password, self.user.password))
        self.assertEqual(self.user.status, UserStatus.ACTIVE, "The user's status was not initialized correctly.")
        self.assertEqual(self.user.user_type, UserTypes.EXTERNAL, "The user's type was not initialized correctly.")
        self.assertIsNotNone(datetime.fromisoformat(self.user.created_at))


    def test_setters_and_getters(self):
        """
        Verify all setters and getters are working for the User entity.
        """
        new_password = "newsecurepassword"
        self.user.first_name = "New"
        self.user.last_name = "User"
        self.user.gender = "Non-binary"
        self.user.birth_date = "1995-05-05"
        self.user.email = "newuser@example.com"
        self.user.phone = "555-9999"
        self.user.password = new_password
        self.user.status = UserStatus.INACTIVE
        self.user.user_type = UserTypes.INTERNAL

        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.gender, "Non-binary")
        self.assertEqual(self.user.birth_date, "1995-05-05")
        self.assertEqual(self.user.email, "newuser@example.com")
        self.assertEqual(self.user.phone, "555-9999")
        self.assertTrue(verify_password(new_password, self.user.password))
        self.assertEqual(self.user.status, UserStatus.INACTIVE)
        self.assertEqual(self.user.user_type, UserTypes.INTERNAL)
    
    def test_str_representation(self):
        """
        Test the __str__ method returns a string with key user information.
        """
        user_str = str(self.user)
        self.assertIn("first_name", user_str)
        self.assertIn("email", user_str)
        self.assertIn("user_status", user_str)
        self.assertIn("user_type", user_str)


if __name__ == '__main__':
    unittest.main()