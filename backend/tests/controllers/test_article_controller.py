import unittest
import os
import json
from datetime import date
import uuid
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
            article_id=uuid.uuid4(),
            content='Test article content',
            image_rel_url='test/image.png'
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
        self.assertEqual(result_id, self.test_article.article_id)

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
        self.assertIsNotNone(articles[0]['article_id'])

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
        found = self.controller.get_by_id(str(self.test_article.article_id))
        self.assertIsNotNone(found)
        self.assertEqual(found['article_id'], str(self.test_article.article_id))

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

    def test_add_multiple_articles(self):
        """
        Test adding multiple articles.
        """
        article2 = Article(
            article_id=uuid.uuid4(),
            content='Second article',
            image_rel_url='test/image2.png'
        )

        self.controller.add(self.test_article)
        self.controller.add(article2)

        articles = self.controller.get_all()
        self.assertEqual(len(articles), 2)
        self.assertIsNotNone(articles[1]['article_id'])
        self.assertEqual(articles[1]['content'], "Second article")

    def test_update_article_success(self):
        """
        Test updating an article that exists.
        """
        self.controller.add(self.test_article)
        updates = {"content": "Updated content"}
        result = self.controller.update_article(str(self.test_article.article_id), updates)
        self.assertTrue(result)

        updated_article = self.controller.get_by_id(str(self.test_article.article_id))
        self.assertEqual(updated_article["content"], "Updated content")

    def test_update_article_not_found(self):
        """
        Test updating an article that does not exist.
        """
        fake_id = str(uuid.uuid4())
        updates = {"content": "New content"}
        result = self.controller.update_article(fake_id, updates)
        self.assertFalse(result)

    def test_delete_article_success(self):
        """
        Test deleting an article that exists.
        """
        self.controller.add(self.test_article)
        result = self.controller.delete_article(str(self.test_article.article_id))
        self.assertTrue(result)

        deleted = self.controller.get_by_id(str(self.test_article.article_id))
        self.assertIsNone(deleted)

    def test_delete_article_not_found(self):
        """
        Test deleting an article that does not exist.
        """
        fake_id = str(uuid.uuid4())
        result = self.controller.delete_article(fake_id)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
