import unittest
import os
import json
from datetime import date
from backend.logic.entities.article import Article
from backend.logic.controllers.article_controller import ArticleController

class TestArticleController(unittest.TestCase):
    """
    Unit tests for the ArticleController class.
    """

    def setUp(self):
        """
        Prepare a temporary test environment by using a test-specific JSON file.
        """
        self.test_file = os.path.join(os.getcwd(), 'backend', 'data', 'test_storage_article.json')
        self.controller = ArticleController()
        self.controller.file = self.test_file  # Override default file with test file

        
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

        self.test_article = Article(
            id=1,
            user_id=123,
            section_id=10,
            content="Test article content",
            created_at=date(2025, 4, 18),
            has_spoiler=False
        )

    def tearDown(self):
        """
        Remove the test file after each test run.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_article(self):
        """
        Test adding an article to the storage.
        """
        result_id = self.controller.add(self.test_article)
        self.assertEqual(result_id, self.test_article.id)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['content'], "Test article content")

    def test_get_all_articles(self):
        """
        Test retrieving all articles from the storage.
        """
        self.controller.add(self.test_article)
        articles = self.controller.get_all()
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['id'], 1)

    def test_get_article_by_id_found(self):
        """
        Test retrieving an article by ID that exists.
        """
        self.controller.add(self.test_article)
        found = self.controller.get_by_id(1)
        self.assertIsNotNone(found)
        self.assertEqual(found['id'], 1)

    def test_get_article_by_id_not_found(self):
        """
        Test retrieving an article by ID that does not exist.
        """
        self.controller.add(self.test_article)
        result = self.controller.get_by_id(999)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
