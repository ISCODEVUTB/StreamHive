import unittest
import json
from unittest.mock import patch, mock_open, MagicMock
from uuid import uuid4
from backend.logic.controllers.profile_controller import ProfileController
from backend.logic.entities.profile import Profile
from backend.logic.entities.profile_roles import ProfileRoles


class TestProfileController(unittest.TestCase):

    def setUp(self):
        self.profile_id = str(uuid4())
        self.profile_data = [{
            "username": "john_doe",
            "description": "I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url": "https://example.com/profile_pic.jpg",
            "profile_role": ProfileRoles.SUBSCRIBER.value,
            "profile_id": self.profile_id
        }]
        self.valid_profile = Profile(
            profile_id=self.profile_id,
            username="janedoe123",
            description="Just another test profile, but I'm a critic.",
            profile_pic_url="https://example.com/pic.jpg",
            profile_role=ProfileRoles.CRITIC,
        )

    @patch("json.dump")
    @patch("builtins.open")
    def test_add_profile_success(self, mock_open_file, mock_json_dump):
        m_open = mock_open(read_data=json.dumps([]))
        mock_open_file.side_effect = [m_open.return_value, m_open.return_value]

        controller = ProfileController()
        result = controller.add(self.valid_profile)

        self.assertEqual(result, self.profile_id)
        self.assertTrue(mock_json_dump.called)

    def test_add_invalid_object(self):
        controller = ProfileController()
        with self.assertRaises(ValueError):
            controller.add("not_a_profile_object")

    @patch("builtins.open")
    def test_get_all_profiles_success(self, mock_open_file):
        m_open = mock_open(read_data=json.dumps(self.profile_data))
        mock_open_file.return_value = m_open.return_value

        controller = ProfileController()
        result = controller.get_all()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "john_doe")

    @patch("builtins.open")
    def test_get_all_profiles_error(self, mock_open_file):
        mock_open_file.side_effect = Exception("File read error")

        controller = ProfileController()
        result = controller.get_all()

        self.assertEqual(result, [])

    @patch("builtins.open")
    def test_get_profile_by_id_success(self, mock_open_file):
        m_open = mock_open(read_data=json.dumps(self.profile_data))
        mock_open_file.return_value = m_open.return_value

        controller = ProfileController()
        result = controller.get_by_id(self.profile_id)

        self.assertIsNotNone(result)
        self.assertEqual(result["profile_id"], self.profile_id)

    @patch("builtins.open")
    def test_get_profile_by_id_not_found(self, mock_open_file):
        m_open = mock_open(read_data=json.dumps(self.profile_data))
        mock_open_file.return_value = m_open.return_value

        controller = ProfileController()
        result = controller.get_by_id("non_existent_id")

        self.assertIsNone(result)

    @patch("builtins.open")
    def test_get_profile_by_id_error(self, mock_open_file):
        mock_open_file.side_effect = Exception("Read error")

        controller = ProfileController()
        result = controller.get_by_id(self.profile_id)

        self.assertIsNone(result)

    @patch("json.dump")
    @patch("builtins.open")
    def test_add_profile_file_error(self, mock_open_file, mock_json_dump):
        mock_open_file.side_effect = Exception("Write error")

        controller = ProfileController()
        result = controller.add(self.valid_profile)

        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()
