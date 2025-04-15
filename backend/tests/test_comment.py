import unittest
from logic.entities.comment import Comment 


class TestComment(unittest.TestCase):
    """
    Test cases for the Comment class.

    This class tests the correct initialization and property behavior
    of the Comment class.
    """

    def setUp(self):
        """
        Set up a Comment object for use in the test case.
        """
        self.comment = Comment(
            id=1,
            user_id=10,
            movie_id=100,
            description="Great movie!",
            created_at="2025-04-14 15:30:00",
            like_by=[2, 3, 4],
            has_spoiler=False
        )
    def test_comment(self):
        """
        Test the initialization of the Comment object.

        Verifies if all attributes of the Comment object are correctly set during initialization.
        """
        self.assertEqual(self.comment.id, 1, "The ID was not initialized correctly.")
        self.assertEqual(self.comment.user_id, 10, "The user_id was not initialized correctly.")
        self.assertEqual(self.comment.movie_id, 100, "The movie_id was not initialized correctly.")
        self.assertEqual(self.comment.description, "Great movie!", "The description was not initialized correctly.")
        self.assertEqual(self.comment.created_at, "2025-04-14 15:30:00", "The created_at was not initialized correctly.")
        self.assertEqual(self.comment.like_by, [2, 3, 4], "The like_by list was not initialized correctly.")
        self.assertFalse(self.comment.has_spoiler, "The has_spoiler flag was not initialized correctly.")

if __name__ == "__main__":
    unittest.main()
