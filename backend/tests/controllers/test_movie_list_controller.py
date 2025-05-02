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
        self.profile_id = str(uuid4())


    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    @patch("json.dump")
    def test_add_movie_list(self, mock_json_dump, mock_open_file, mock_exists):
        controller = MovieListController()

        new_movie_list = MovieList(
            id=str(uuid4()),
            profile_id=self.profile_id,
        )

        result = controller.add(new_movie_list)

        self.assertGreaterEqual(mock_open_file.call_count, 1)
        mock_json_dump.assert_called_once()

        args, _ = mock_json_dump.call_args
        dumped_data = args[0]
        self.assertEqual(result, new_movie_list)


    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "profile_id": "some-user",
        "movies": [101, 102, 103]
    }]))
    def test_get_all(self, mock_open_file, mock_exists):
        controller = MovieListController()
        result = controller.get_all()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["profile_id"], "some-user")
        self.assertGreaterEqual(mock_open_file.call_count, 1)


    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "profile_id": "some-user",
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
    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "profile_id": "some-user",
        "movies": [{"movie_id": "101", "added_at": "2025-04-25T00:00:00"}]
    }]))
    def test_add_movie(self, mock_open_file, mock_json_dump, mock_exists):
        controller = MovieListController()

        # Simulando que la película que se va a agregar tiene el ID "102"
        movie_id = "102"
        movie_list_id = "some-id"

        # Realizando la operación
        exp = controller.add_movie(movie_list_id, movie_id)
        self.assertTrue(exp)

        # Verificando que la nueva película se haya agregado a la lista
        written_data = mock_json_dump.call_args[0][0]
        movie_list = next((m for m in written_data if m["id"] == movie_list_id), None)
        self.assertIsNotNone(movie_list)
        self.assertTrue(any(m["movie_id"] == movie_id for m in movie_list["movies"]))


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "profile_id": "some-user",
        "movies": [{"movie_id": "101", "added_at": "2025-04-25T00:00:00"}]
    }]))
    def test_add_movie_exists(self, mock_file):
        controller = MovieListController()

        movie_id = "101"
        movie_list_id = "some-id"

        exp = controller.add_movie(movie_list_id, movie_id)

        self.assertFalse(exp)
        

    @patch("os.path.exists", return_value=True)
    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "profile_id": "some-user",
        "movies": [
            {"movie_id": "101", "added_at": "2025-04-25T00:00:00"},
            {"movie_id": "102", "added_at": "2025-04-26T00:00:00"}
        ]
    }]))
    def test_remove_movie(self, mock_open_file, mock_json_dump, mock_exists):
        controller = MovieListController()

        # Simulando que la película que se va a eliminar tiene el ID "102"
        movie_id = "102"
        movie_list_id = "some-id"

        # Realizando la operación
        controller.remove_movie(movie_list_id, movie_id)

        written_data = mock_json_dump.call_args[0][0]
        movie_list = next((m for m in written_data if m["id"] == movie_list_id), None)
        self.assertIsNotNone(movie_list)
        self.assertFalse(any(m["movie_id"] == movie_id for m in movie_list["movies"]))


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
        "id": "some-id",
        "profile_id": "some-user",
        "movies": [{"movie_id": "101", "added_at": "2025-04-25T00:00:00"}]
    }]))
    def test_remove_movie_not_found(self, mock_file):
        controller = MovieListController()

        # La película que se intenta eliminar no existe en la lista
        movie_id = "999"
        movie_list_id = "some-id"

        # Realizando la operación
        exp = controller.remove_movie(movie_list_id, movie_id)

        # Verificando que no se haya modificado el archivo porque la película no existe
        self.assertFalse(exp)


if __name__ == '__main__':
    unittest.main()
    