import unittest
import os
import json
from unittest.mock import patch, mock_open
from uuid import uuid4
from backend.logic.controllers.profile_controller import ProfileController
from backend.logic.entities.profile import Profile
from backend.logic.entities.profile_roles import ProfileRoles


class TestProfileController(unittest.TestCase):
    def setUp(self):
        self.profile_id = str(uuid4())
        self.profile_data = Profile(
            username="john_doe",
            description="I'm John Doe, I love horror and romance movies, this is a test profile.",
            profile_pic_url="https://example.com/profile_pic.jpg",
            profile_role=ProfileRoles.SUBSCRIBER,
            profile_id=self.profile_id
        )
    
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    @patch("json.dump")
    def test_add_profile(self, mock_json_dump, mock_open_file):
        controller = ProfileController()

        new_profile = Profile(
            profile_id=str(uuid4()),
            username="janedoe123",
            description="Just another test profile, but I'm a critic.",
            profile_pic_url="https://example.com/pic.jpg",
            profile_role=ProfileRoles.CRITIC,
        )

        result = controller.add(new_profile)
    
        mock_open_file.assert_called_once_with(controller.file, 'r+', encoding='utf-8')
        mock_json_dump.assert_called_once()  # Se asegura de que json.dump se ejecutó
        args, _ = mock_json_dump.call_args
        dumped_data = args[0]  # Los datos que se pasaron a json.dump
        self.assertIn(new_profile.to_dict(), dumped_data)  # Verificar que el perfil nuevo está en los datos
        self.assertEqual(result, new_profile)
    
    def test_add_profile_with_invalid_object(self):
        controller = ProfileController()
        with self.assertRaises(ValueError):
            controller.add("no_es_un_perfil")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_get_all(self, mock_open_file, mock_exists):
        test_data = [{
            "username": "john_doe",
            "description": "I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url": "https://example.com/profile_pic.jpg",
            "profile_role": ProfileRoles.SUBSCRIBER.value,
            "profile_id": self.profile_id
        }]

        mock_open_file().read.return_value = json.dumps(test_data)

        controller = ProfileController()
        result = controller.get_all()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "john_doe")




    @patch("builtins.open")
    def test_get_profile_by_id(self, mock_open_file):
        test_data = [{
            "username": "john_doe",
            "description": "I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url": "https://example.com/profile_pic.jpg",
            "profile_role": ProfileRoles.SUBSCRIBER.value,
            "profile_id": self.profile_id
        }]
        mock_open_file.return_value = mock_open(read_data=json.dumps(test_data)).return_value

        controller = ProfileController()
        result = controller.get_by_id(self.profile_id)

        self.assertIsNotNone(result)
        self.assertEqual(result["profile_id"], self.profile_id)

    @patch("builtins.open")
    def test_get_profile_by_id_not_found(self, mock_open_file):
        test_data = [{
            "username": "john_doe",
            "description": "I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url": "https://example.com/profile_pic.jpg",
            "profile_role": ProfileRoles.SUBSCRIBER.value,
            "profile_id": self.profile_id
        }]
        mock_open_file.return_value = mock_open(read_data=json.dumps(test_data)).return_value

        controller = ProfileController()
        result = controller.get_by_id("non-existent-id")

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
