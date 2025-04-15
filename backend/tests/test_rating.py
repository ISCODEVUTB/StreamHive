import unittest
from datetime import date
from backend.logic.entities.rating import Rating


class TestRating(unittest.TestCase):
    """
    Test cases for the Rating class.

    The TestRating class contains unit tests that verify the behavior 
    and functionality of the Rating class methods.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a sample Rating object.
        """
        self.rating = Rating(
            profile_id=12345,
            movie_id=67890,
            rate = 4.5,
            created_at=datetime(2025, 4, 11, 14, 30) 
        )

    def test_rate_value_error(self):
        """
        Verify that a ValueError is raissed when the rate is not between 0 and 5
        """
        with self.assertRaises(
            ValueError, msg="The rating must be a value between 0 and 5"
        ):
            self.rate.rate = "2025-04-11"

    def test_created_at_type_error(self):
        """
        Verify that a TypeError is raised when the value's type is not datetime
        """
        with self.assertRaises(
            TypeError, msg="The created at must be a datetime type"
        ):
            self.rate.created_at = "2025-04-11 14:30"


    def test_rating_initialization(self):
        """
        Test the initialization of the Rating object.
    
        Verifies if all attributes of the Rating object are correctly set during initialization.
        """
        self.assertEqual(self.rating.profile_id, 12345, "The profile ID was not initialized correctly.")
        self.assertEqual(self.rating.movie_id, 0, "The movie ID was not initialized correctly.")
        self.assertEqual(self.rating.rate, 4.5, "The rate was not initialized correctly.")
        self.assertEqual(self.rating.created_at, datetime(2025, 4, 11, 14, 30), "The created_at was not initialized correctly.")

if __name__ == '__main__':
    unittest.main()
