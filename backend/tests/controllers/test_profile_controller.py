import unittest
import json
from unittest.mock import patch, mock_open
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

    @patch("json.dump")
    @patch("builtins.open")
    def test_add_profile(self, mock_open_file, mock_json_dump):
        m_open = mock_open(read_data=json.dumps([]))
        mock_open_file.side_effect = [m_open.return_value, m_open.return_value]

        controller = ProfileController()
        new_profile = Profile(
            profile_id=self.profile_id,
            username="janedoe123",
            description="Just another test profile, but I'm a critic.",
            profile_pic_url="https://example.com/pic.jpg",
            profile_role=ProfileRoles.CRITIC,
        )

        result = controller.add(new_profile)

        self.assertEqual(result, self.profile_id)
        self.assertTrue(mock_json_dump.called)

    @patch("builtins.open")
    def test_get_all(self, mock_open_file):
        m_open = mock_open(read_data=json.dumps(self.profile_data))
        mock_open_file.return_value = m_open.return_value

        controller = ProfileController()
        result = controller.get_all()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "john_doe")

    @patch("builtins.open")
    def test_get_profile_by_id(self, mock_open_file):
        m_open = mock_open(read_data=json.dumps(self.profile_data))
        mock_open_file.return_value = m_open.return_value

        controller = ProfileController()
        result = controller.get_by_id(self.profile_id)

        self.assertIsNotNone(result)
        self.assertEqual(result["profile_id"], self.profile_id)

if __name__ == '__main__':
    unittest.main()
