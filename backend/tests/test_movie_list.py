import unittest
from logic.entities.movie_list import MovieList


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
            id=1,
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
        self.assertEqual(self.movie_list.id, 1, "The ID was not initialized correctly.")
        self.assertEqual(self.movie_list.user_id, 10, "The user_id was not initialized correctly.")
        self.assertEqual(self.movie_list.privacy, "public", "The privacy setting was not initialized correctly.")
        self.assertEqual(self.movie_list.list_name, "Top Movies 2025", "The list_name was not initialized correctly.")
        self.assertEqual(self.movie_list.list_description, "A list of my favorite movies from 2025", "The list_description was not initialized correctly.")
        self.assertEqual(self.movie_list.like_by, [2, 3], "The like_by list was not initialized correctly.")
        self.assertEqual(self.movie_list.saved_by, [4, 5], "The saved_by list was not initialized correctly.")
        self.assertEqual(self.movie_list.movies, [1001, 1002, 1003], "The movies list was not initialized correctly.")

if __name__ == "__main__":
    unittest.main()
