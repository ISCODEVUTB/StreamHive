import unittest
import os
import json
from unittest.mock import patch, mock_open
from uuid import uuid4
from backend.logic.controllers.movie_list_controller import MovieListController
from backend.logic.entities.movie_list import MovieList

class TestMovieListController(unittest.TestCase):

    def setUp(self):
        self.example_id = str(uuid4())
        self.user_id = str(uuid4())

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    @patch("json.dump")
    def test_add_movie_list(self, mock_json_dump, mock_open_file, mock_exists):
        controller = MovieListController()

        new_movie_list = MovieList(
            id=str(uuid4()),
            user_id=self.user_id,
            privacy="private",
            list_name="New Movie List",
            list_description="A description made by the user of the movie list",
            like_by=[1],
            saved_by=[2],
            movies=[104, 105]
        )

        result = controller.add(new_movie_list)

        self.assertGreaterEqual(mock_open_file.call_count, 1)
        mock_json_dump.assert_called_once()

        args, _ = mock_json_dump.call_args
        dumped_data = args[0]
        self.assertTrue(any(entry["list_name"] == "New Movie List" for entry in dumped_data))
        self.assertEqual(result, new_movie_list)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "user_id": "some-user",
        "privacy": "private",
        "list_name": "Favorites",
        "list_description": "Your favorite movies in one place.",
        "like_by": [1, 2],
        "saved_by": [3],
        "movies": [101, 102, 103]
    }]))
    def test_get_all(self, mock_open_file, mock_exists):
        controller = MovieListController()
        result = json.loads(controller.get_all())

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["list_name"], "Favorites")
        self.assertGreaterEqual(mock_open_file.call_count, 1)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "user_id": "some-user",
        "privacy": "private",
        "list_name": "Favorites",
        "list_description": "Your favorite movies in one place.",
        "like_by": [1, 2],
        "saved_by": [3],
        "movies": [101, 102, 103]
    }]))
    def test_get_movie_list_by_id(self, mock_open_file, mock_exists):
        controller = MovieListController()
        result = controller.get_by_id("some-id")

        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "some-id")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_get_movie_list_by_id_not_found(self, mock_open_file, mock_exists):
        controller = MovieListController()
        result = controller.get_by_id("non-existent-id")
        self.assertIsNone(result)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "user_id": "some-user",
        "privacy": "private",
        "list_name": "Favorites",
        "list_description": "Your favorite movies in one place.",
        "like_by": [1, 2],
        "saved_by": [3],
        "movies": [101, 102, 103]
    }]))
    @patch("json.dump")
    def test_update_movie_list(self, mock_json_dump, mock_open_file, mock_exists):
        controller = MovieListController()
        updated_movie_list = MovieList(
            id="some-id",
            user_id="some-user",
            privacy="private",
            list_name="Updated List",
            list_description="Updated description",
            like_by=[2],
            saved_by=[3],
            movies=[200, 201]
        )

        result = controller.update("some-id", updated_movie_list)

        self.assertTrue(result)
        self.assertGreaterEqual(mock_open_file.call_count, 1)
        mock_json_dump.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "user_id": "some-user",
        "privacy": "private",
        "list_name": "Favorites",
        "list_description": "Your favorite movies in one place.",
        "like_by": [1, 2],
        "saved_by": [3],
        "movies": [101, 102, 103]
    }]))
    @patch("json.dump")
    def test_update_movie_list_not_found(self, mock_json_dump, mock_open_file, mock_exists):
        controller = MovieListController()
        non_existent_id = str(uuid4())
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
        self.assertGreaterEqual(mock_open_file.call_count, 1)
        mock_json_dump.assert_not_called()

if __name__ == '__main__':
    unittest.main()