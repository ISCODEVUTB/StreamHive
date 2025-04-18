import unittest
import os
import json
from backend.logic.controllers.comment_controller import CommentController
from backend.logic.entities.comment import Comment

class TestCommentController(unittest.TestCase):

    def setUp(self):
        # Inicializa el controlador y limpia el archivo antes de cada prueba
        self.controller = CommentController()
        self.test_file = self.controller.file
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def test_add_and_get_all(self):
        comment = Comment(
            id=1,
            user_id=101,
            movie_id=202,
            description="Una peli brutal",
            created_at="2025-04-18 12:00:00",
            like_by=[45, 67],
            has_spoiler=False
        )

        # Agrega comentario
        result = self.controller.add(comment)
        self.assertEqual(result.id, comment.id)

        # Verifica que show devuelve algo
        result_show = self.controller.get_all()
        self.assertIn("Una peli brutal", result_show)

    def test_get_by_id(self):
        comment = Comment(
            id=99,
            user_id=101,
            movie_id=202,
            description="Comentario único",
            created_at="2025-04-18 12:30:00",
            like_by=[],
            has_spoiler=True
        )

        self.controller.add(comment)
        found = self.controller.get_by_id(99)
        self.assertIsNotNone(found)
        self.assertEqual(found["id"], 99)
        self.assertEqual(found["description"], "Comentario único")

if __name__ == '__main__':
    unittest.main()
