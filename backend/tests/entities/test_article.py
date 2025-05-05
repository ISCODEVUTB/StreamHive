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
        self.article_id=uuid.uuid4()
        self.article = Article(
            article_id=self.article_id,
            content='Sample content',
            image_rel_url='test/image.png'
        )

    def test_article_id(self):
        """
        Test that the article ID is correctly generated as a UUID.
        """
        self.assertIsInstance(self.article.article_id, uuid.UUID, "The ID is not a valid UUID.")

    def test_article_initialization(self):
        """
        Test the initialization of the Article object.
    
        Verifies if all attributes of the Article object are correctly set during initialization.
        """
        self.assertEqual(self.article.article_id, self.article_id, "The user ID was not initialized correctly.")
        self.assertEqual(self.article.content, "Sample content", "The content was not initialized correctly.")
        self.assertEqual(self.article.image_rel_url, "test/image.png", "The content was not initialized correctly.")

    def test_setters_and_getters(self):
        """
        Test the setters and getters of the Article object.
        """
        self.article.content = "New content"
        self.article.image_rel_url = "test/image3.png"

        self.assertIsNotNone(self.article.article_id)
        self.assertEqual(self.article.content, "New content")
        self.assertEqual(self.article.image_rel_url, "test/image3.png")

if __name__ == '__main__':
    unittest.main()
    