import unittest
import os
import json
from unittest.mock import patch, mock_open
from uuid import uuid4
from backend.logic.controllers.movie_list_controller import MovieListController
from backend.logic.entities.movie_list import MovieList

class TestMovieListController(unittest.TestCase):

    def setUp(self):
        """
        Set up IDs and dummy movie list data for testing.
        """
        self.example_id = str(uuid.uuid4())
        self.user_id = str(uuid.uuid4())

        self.movie_list_data = [{
            "id": self.example_id,
            "user_id": self.user_id,
            "privacy": "public",
            "list_name": "Favorite Movies",
            "list_description": "Your favorites movies in one place.",
            "like_by": [1, 2],
            "saved_by": [3],
            "movies": [101, 102, 103]
        }]

    @patch(
        "builtins.open", 
        new_callable=mock_open, 
        read_data=json.dumps([])
    )
    @patch("json.dump")
    def test_add_movie_list(self, mock_json_dump, mock_open_file):
        """
        Test adding a new MovieList to storage.
        Ensures the object is saved and returned correctly.
        """
        controller = MovieListController()
        
        new_movie_list = MovieList(
            user_id=self.user_id,
            privacy="private",
            list_name="New Movie List",
            list_description="A description made by the user of the movie list",
            like_by=[1],
            saved_by=[2],
            movies=[104, 105]
        )

        result = controller.add(new_movie_list)

        mock_open_file.assert_called_once_with(controller.file, 'r+', encoding='utf-8')
        mock_json_dump.assert_called_once()  
        self.assertEqual(result, new_movie_list)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{
            "id": self.example_id,
            "user_id": self.user_id,
            "privacy": "private",
            "list_name": "Favorites",
            "list_description": "Your favorite movies in one place.",
            "like_by": [1, 2],
            "saved_by": [3],
            "movies": [101, 102, 103]
        }])
    )
    def test_get_all(self, mock_open_file):
        """
        Test retrieving all movie lists from storage.
        Checks if data is properly loaded and returned.
        """
        controller = MovieListController()
        result = controller.get_all()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["list_name"], "Favorites")
        mock_open_file.assert_called_once_with(controller.file, 'r')

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{
            "id": self.example_id,
            "user_id": self.user_id,
            "privacy": "private",
            "list_name": "Favorites",
            "list_description": "Your favorite movies in one place.",
            "like_by": [1, 2],
            "saved_by": [3],
            "movies": [101, 102, 103]
        }])
    )
    def test_get_movie_list_by_id(self, mock_open_file):
        """
        Test retrieving a specific MovieList by its UUID.
        Validates that the correct movie list is returned.
        """
        controller = MovieListController()
        result = controller.get_by_id(self.example_id)

        self.assertIsNotNone(result)
        self.assertEqual(result["id"], self.example_id)

    @patch(
        "builtins.open", 
        new_callable=mock_open, 
        read_data=json.dumps([{
            "id": self.example_id,
            "user_id": self.user_id,
            "privacy": "private",
            "list_name": "Favorites",
            "list_description": "Your favorite movies in one place.",
            "like_by": [1, 2],
            "saved_by": [3],
            "movies": [101, 102, 103]
        }])
    )
    @patch("json.dump")
    def test_update_movie_list(self, mock_json_dump, mock_open_file):
        """
        Test updating an existing MovieList.
        Confirms that the update is saved and successful.
        """
        controller = MovieListController()
        updated_movie_list = MovieList(
            id=self.example_id,
            user_id=self.user_id,
            privacy="private",
            list_name="Updated List",
            list_description="Updated description",
            like_by=[2],
            saved_by=[3],
            movies=[200, 201]
        )

        result = controller.update(self.example_id, updated_movie_list)

        self.assertTrue(result)
        mock_open_file.assert_called_once_with(controller.file, 'r+', encoding='utf-8')
        mock_json_dump.assert_called_once()

    @patch(
        "builtins.open", 
        new_callable=mock_open, 
        read_data=json.dumps([{
            "id": self.example_id,
            "user_id": self.user_id,
            "privacy": "private",
            "list_name": "Favorites",
            "list_description": "Your favorite movies in one place.",
            "like_by": [1, 2],
            "saved_by": [3],
            "movies": [101, 102, 103]
        }])
    )
    @patch("json.dump")
    def test_update_movie_list_not_found(self, mock_json_dump, mock_open_file):
        """
        Test trying to update a MovieList with an ID that doesn't exist.
        Ensures the method returns False and doesn't call json.dump.
        """
        controller = MovieListController()
        non_existent_id = str(uuid.uuid4())
        updated_movie_list = MovieList(
            id=non_existent_id,
            user_id=self.user_id,
            privacy="private",
            list_name="Should Not Update",
            list_description="This shouldn't be saved",
            like_by=[],
            saved_by=[],
            movies=[]
        )

        result = controller.update(non_existent_id, updated_movie_list)

        self.assertFalse(result)
        mock_open_file.assert_called_once_with(controller.file, 'r+', encoding='utf-8')
        mock_json_dump.assert_not_called()

if __name__ == '__main__':
    unittest.main()

