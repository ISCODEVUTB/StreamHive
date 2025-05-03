import unittest
import os
import json
from backend.logic.controllers.comment_controller import CommentController
from backend.logic.entities.comment import Comment

class TestCommentController(unittest.TestCase):
    def setUp(self):
        # Archivo temporal para pruebas
        self.test_file = os.path.join(os.getcwd(), 'backend', 'data', 'test_storage.json')
        self.controller = CommentController()
        self.controller.file = self.test_file  # Redirigir al archivo temporal

        # Asegurar limpieza del archivo
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

        self.comment = Comment(
            id=1,
            user_id=10,
            movie_id=100,
            description="Muy buena peli!",
            created_at="2025-04-18T12:00:00",
            like_by=[5, 6],
            has_spoiler=False
        )

    def tearDown(self):
        # Eliminar archivo de prueba al final
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_comment(self):
        result = self.controller.add(self.comment)
        self.assertEqual(result.id, 1)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["description"], "Muy buena peli!")

    def test_get_all(self):
        self.controller.add(self.comment)
        all_comments = self.controller.get_all()
        self.assertIn("Muy buena peli!", all_comments)

    def test_get_by_id(self):
        self.controller.add(self.comment)
        found = self.controller.get_by_id(1)
        self.assertIsNotNone(found)
        self.assertEqual(found["user_id"], 10)

        not_found = self.controller.get_by_id(999)
        self.assertIsNone(not_found)


if __name__ == '__main__':
    unittest.main()