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
        """
        Set up IDs and dummy profile data for testing.
        """
        self.profile_id = str(uuid.uuid4())

        self.profile_data = [{
            "username":"john_doe",
            "description":"I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url":"https://example.com/profile_pic.jpg",
            "profile_role":ProfileRoles.SUBSCRIBER.value,
            "profile_id":self.profile_id 
        }]

    @patch(
        "builtins.open", 
        new_callable=mock_open, 
        read_data=json.dumps([])
    )
    @patch("json.dump")
    def test_add_profile(self, mock_json_dump, mock_open_file):
        """
        Test adding a new Profile to storage.
        Ensures the object is saved and returned correctly.
        """
        controller = ProfileController()
        
        new_profile = Profile(
            profile_id=self.profile_id,
            username="janedoe123",
            description="Just another test profile, but I'm a critic.",
            profile_pic_url="https://example.com/pic.jpg",
            profile_role=ProfileRoles.CRITIC,
        )

        result = controller.add(new_profile)

        mock_open_file.assert_called_once_with(controller.file, 'r+', encoding='utf-8')
        mock_json_dump.assert_called_once()  
        self.assertEqual(result, new_profile)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{
            "username":"john_doe",
            "description":"I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url":"https://example.com/profile_pic.jpg",
            "profile_role":ProfileRoles.SUBSCRIBER.value,
            "profile_id":self.profile_id 
        }])
    )
    def test_get_all(self, mock_open_file):
        """
        Test retrieving all profiles from storage.
        Checks if data is properly loaded and returned.
        """
        controller = ProfileController()
        result = controller.get_all()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "john_doe")
        mock_open_file.assert_called_once_with(controller.file, 'r')

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{
            "username":"john_doe",
            "description":"I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url":"https://example.com/profile_pic.jpg",
            "profile_role":ProfileRoles.SUBSCRIBER.value,
            "profile_id":self.profile_id 
        }])
    )
    def test_get_profile_by_id(self, mock_open_file):
        """
        Test retrieving a specific Profile by its UUID.
        Validates that the correct profile is returned.
        """
        controller = ProfileController()
        result = controller.get_by_id(self.profile_id)

        self.assertIsNotNone(result)
        self.assertEqual(result["profile_id"], self.profile_id)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{
            "username":"john_doe",
            "description":"I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url":"https://example.com/profile_pic.jpg",
            "profile_role":ProfileRoles.SUBSCRIBER.value,
            "profile_id":self.profile_id 
        }])
    )
    @patch("json.dump")
    def test_update_profile(self, mock_json_dump, mock_open_file):
        """
        Test updating an existing Profile.
        Confirms that the update is saved and successful.
        """
        controller = ProfileController()
        updated_profile = Profile(
            profile_id=self.profile_id,
            username="janedoe",
            description="Updated test profile, but I'm a critic.",
            profile_pic_url="https://example.com/pic.jpg",
            profile_role=ProfileRoles.CRITIC,
        )

        result = controller.update(self.profile_id, updated_profile)

        self.assertTrue(result)
        mock_open_file.assert_called_once_with(controller.file, 'r+', encoding='utf-8')
        mock_json_dump.assert_called_once()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{
            "username":"john_doe",
            "description":"I'm John Doe, I love horror and romance movies, this is a test profile.",
            "profile_pic_url":"https://example.com/profile_pic.jpg",
            "profile_role":ProfileRoles.SUBSCRIBER.value,
            "profile_id":self.profile_id 
        }])
    )
    @patch("json.dump")
    def test_update_profile_not_found(self, mock_json_dump, mock_open_file):
        """
        Test trying to update a Profile with an ID that doesn't exist.
        Ensures the method returns False and doesn't call json.dump.
        """
        controller = ProfileController()
        non_existent_id = str(uuid.uuid4())
        updated_profile = Profile(
            profile_id=non_existent_id,
            username="janedoe",
            description="Should Not Update test profile, but I'm a critic.",
            profile_pic_url="https://example.com/pic.jpg",
            profile_role=ProfileRoles.CRITIC,
        )

        result = controller.update(non_existent_id, updated_profile)

        self.assertFalse(result)
        mock_open_file.assert_called_once_with(controller.file, 'r+', encoding='utf-8')
        mock_json_dump.assert_not_called()

if __name__ == '__main__':
    unittest.main()

