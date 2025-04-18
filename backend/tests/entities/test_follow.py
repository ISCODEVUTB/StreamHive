import unittest
from datetime import datetime
from backend.logic.entities.follow import Follow


class TestFollow(unittest.TestCase):
    """
    Test cases for the Follow class.

    The TestFollow class contains unit tests that verify the behavior 
    and functionality of the Follow class methods.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a sample Follow object.
        """
        self.follow = Follow(
            follower_id=12345,
            following_id=67890,
            created_at=datetime(2025, 4, 11, 14, 30) 
        )

    def test_created_at_type_error(self):
        """
        Verify that a TypeError is raised when the value's type is not datetime
        """
        with self.assertRaises(
            TypeError, msg="The created at must be a datetime type"
        ):
            self.follow.created_at = "2025-04-11 14:30"

    def test_follow_initialization(self):
        """
        Test the initialization of the Follow object.
    
        Verifies if all attributes of the Follow object are correctly set during initialization.
        """
        self.assertEqual(self.follow.follower_id, 12345, "The follower ID was not initialized correctly.")
        self.assertEqual(self.follow.following_id, 67890, "The following ID was not initialized correctly.")
        self.assertEqual(self.follow.created_at, datetime(2025, 4, 11, 14, 30), "The created_at was not initialized correctly.")

if __name__ == '__main__':
    unittest.main()
