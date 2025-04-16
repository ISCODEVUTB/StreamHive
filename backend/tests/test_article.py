import unittest
from datetime import date
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
        self.article = Article(
            id=1,
            user_id=12345,
            section_id=0,
            content="Sample content",
            created_at=date(2025, 4, 11),
            has_spoiler=False
        )

    def test_created_at_type_error(self):
        """
        Verify that a TypeError is raised when 
        """
        with self.assertRaises(
            TypeError, msg="The created at must be a date type"
        ):
            self.article.created_at = "2025-04-11"

    def test_article_initialization(self):
        """
        Test the initialization of the Article object.
    
        Verifies if all attributes of the Article object are correctly set during initialization.
        """
        self.assertEqual(self.article.id, 1, "The ID was not initialized correctly.")
        self.assertEqual(self.article.user_id, 12345, "The user ID was not initialized correctly.")
        self.assertEqual(self.article.section_id, 0, "The section ID was not initialized correctly.")
        self.assertEqual(self.article.created_at, date(2025, 4, 11), "The created_at was not initialized correctly.") 
        self.assertFalse(self.article.has_spoiler, "The has_spoiler flag was not initialized correctly.")

    def test_setters_and_getters(self):
        """
        Test the setters and getters of the Article object.
        """
        self.article.id = 2
        self.article.user_id = 124
        self.article.section_id = 457
        self.article.created_at = date(2025, 5, 1)
        self.article.has_spoiler = False

        self.assertEqual(self.article.id, 2)
        self.assertEqual(self.article.user_id, 124)
        self.assertEqual(self.article.section_id, 457)
        self.assertEqual(self.article.created_at, date(2025, 5, 1))
        self.assertFalse(self.article.has_spoiler)

if __name__ == '__main__':
    unittest.main()
