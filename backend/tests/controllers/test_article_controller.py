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

    def test_add_invalid_object(self):
        """
        Test adding an invalid object (not an Article).
        """
        with self.assertRaises(ValueError):
            self.controller.add("esto no es un artículo")

    def test_get_all_articles(self):
        """
        Test retrieving all articles from the storage.
        """
        self.controller.add(self.test_article)
        articles = self.controller.get_all()
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['id'], 1)

    def test_get_all_with_corrupt_file(self):
        """
        Test get_all when the JSON file is corrupt.
        """
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("{ esto no es JSON válido ")

        articles = self.controller.get_all()
        self.assertEqual(articles, [])

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

    def test_get_article_by_id_with_corrupt_file(self):
        """
        Test get_by_id when the file is corrupt.
        """
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("{ archivo roto ")

        result = self.controller.get_by_id(1)
        self.assertIsNone(result)

    def test_created_at_serialization(self):
        """
        Test that created_at is serialized as a string in the stored JSON.
        """
        self.controller.add(self.test_article)
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertIsInstance(data[0]['created_at'], str)

    def test_add_multiple_articles(self):
        """
        Test adding multiple articles.
        """
        article2 = Article(
            id=2,
            user_id=456,
            section_id=11,
            content="Second article",
            created_at=date(2025, 4, 19),
            has_spoiler=True
        )

        self.controller.add(self.test_article)
        self.controller.add(article2)

        articles = self.controller.get_all()
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[1]['id'], 2)
        self.assertEqual(articles[1]['content'], "Second article")


if __name__ == '__main__':
    unittest.main()
