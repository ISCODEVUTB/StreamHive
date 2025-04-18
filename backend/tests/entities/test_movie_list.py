import unittest
from backend.logic.entities.movie_list import MovieList


class TestMovieList(unittest.TestCase):
    """
    Test cases for the MovieList class.

    This class tests the correct initialization and property behavior
    of the MovieList class.
    """

    def setUp(self):
        """
        Set up a MovieList object to use in the test case.
        """
        self.movie_list = MovieList(
            id=None,
            user_id=10,
            privacy="public",
            list_name="Top Movies 2025",
            list_description="A list of my favorite movies from 2025",
            like_by=[2, 3],
            saved_by=[4, 5],
            movies=[1001, 1002, 1003]
        )

    def test_movie_list_initialization(self):
        """
        Test the initialization of the MovieList object.

        Verifies if all attributes of the MovieList object are correctly set during initialization.
        """
        self.assertIsInstance(self.movie_list.id, str, "The ID should be a string.")
        self.assertEqual(self.movie_list.user_id, 10, "The user_id was not initialized correctly.")
        self.assertEqual(self.movie_list.privacy, "public", "The privacy setting was not initialized correctly.")
        self.assertEqual(self.movie_list.list_name, "Top Movies 2025", "The list_name was not initialized correctly.")
        self.assertEqual(self.movie_list.list_description, "A list of my favorite movies from 2025", "The list_description was not initialized correctly.")
        self.assertEqual(self.movie_list.like_by, [2, 3], "The like_by list was not initialized correctly.")
        self.assertEqual(self.movie_list.saved_by, [4, 5], "The saved_by list was not initialized correctly.")
        self.assertEqual(self.movie_list.movies, [1001, 1002, 1003], "The movies list was not initialized correctly.")

    def test_setters_and_getters(self):
        """
        Verify all setters and getters are working.
        """
        self.movie_list.user_id = 20
        self.movie_list.privacy = "private"
        self.movie_list.list_name = "Sci-fi Hits"
        self.movie_list.list_description = "Best sci-fi films ever"
        self.movie_list.like_by = [1, 4]
        self.movie_list.saved_by = [6]
        self.movie_list.movies = [2001, 2002]

        self.assertEqual(self.movie_list.user_id, 20)
        self.assertEqual(self.movie_list.privacy, "private")
        self.assertEqual(self.movie_list.list_name, "Sci-fi Hits")
        self.assertEqual(self.movie_list.list_description, "Best sci-fi films ever")
        self.assertEqual(self.movie_list.like_by, [1, 4])
        self.assertEqual(self.movie_list.saved_by, [6])
        self.assertEqual(self.movie_list.movies, [2001, 2002])

    def test_list_name_length_validation(self):
        """
        Test the validation of list name length.
        """
        with self.assertRaises(ValueError):
            self.movie_list.list_name = "A" * 201  # Exceeds max length of 200 characters

    def test_list_description_length_validation(self):
        """
        Test the validation of list description length.
        """
        with self.assertRaises(ValueError):
            self.movie_list.list_description = "A" * 1001  # Exceeds max length of 1000 characters

    def test_privacy_validation(self):
        """
        Test the validation of privacy setting.
        """
        with self.assertRaises(ValueError):
            self.movie_list.privacy = "restricted"  # Invalid privacy setting

if __name__ == "__main__":
    unittest.main()
