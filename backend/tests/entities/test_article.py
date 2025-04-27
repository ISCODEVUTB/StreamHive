import unittest
import uuid
from datetime import datetime
from backend.logic.entities.article import Article


class TestArticle(unittest.TestCase):
    """
    Test cases for the Article class.

    The TestArticle class contains unit tests that verify the behavior and functionality
    of the Article class methods.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a sample Article object.
        """
        self.user_id = uuid.uuid4()
        self.article = Article(
            user_id=self.user_id,
            section_id=0,
            content="Sample content",
            created_at=datetime(2025, 4, 11, 14, 30),
            has_spoiler=False
        )

    def test_created_at_type_error(self):
        """
        Verify that a TypeError is raised when 
        """
        with self.assertRaises(
            TypeError, msg="The created at must be a datetime object"
        ):
            self.article.created_at = "2025-04-11"

    def test_article_id(self):
        """
        Test that the article ID is correctly generated as a UUID.
        """
        self.assertIsInstance(self.article.id, uuid.UUID, "The ID is not a valid UUID.")

    def test_article_initialization(self):
        """
        Test the initialization of the Article object.
    
        Verifies if all attributes of the Article object are correctly set during initialization.
        """
        self.assertEqual(self.article.user_id, self.user_id, "The user ID was not initialized correctly.")
        self.assertEqual(self.article.section_id, 0, "The section ID was not initialized correctly.")
        self.assertEqual(self.article.created_at, datetime(2025, 4, 11, 14, 30), "The created_at was not initialized correctly.")
        self.assertFalse(self.article.has_spoiler, "The has_spoiler flag was not initialized correctly.")
        self.assertEqual(self.article.content, "Sample content", "The content was not initialized correctly.")

    def test_setters_and_getters(self):
        """
        Test the setters and getters of the Article object.
        """
        new_user_id = uuid.uuid4()
        self.article.user_id = new_user_id
        self.article.section_id = 457
        self.article.created_at = datetime(2025, 5, 1, 10, 30)
        self.article.has_spoiler = False
        self.article.content = "New content"

        self.assertEqual(self.article.user_id, new_user_id)
        self.assertEqual(self.article.section_id, 457)
        self.assertEqual(self.article.created_at, datetime(2025, 5, 1, 10, 30))
        self.assertFalse(self.article.has_spoiler)
        self.assertEqual(self.article.content, "New content")

if __name__ == '__main__':
    unittest.main()
    