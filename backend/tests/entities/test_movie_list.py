import unittest
from uuid import uuid4
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
        self.example_id = str(uuid4())
        self.profile_id = str(uuid4())

        self.movie_list = MovieList(
            id=self.example_id,
            profile_id=self.profile_id
        )

    def test_movie_list_initialization(self):
        """
        Test the initialization of the MovieList object.

        Verifies if all attributes of the MovieList object are correctly set during initialization.
        """
        self.assertEqual(self.movie_list.id, self.example_id, "The ID should be a string.")
        self.assertEqual(self.movie_list.profile_id, self.profile_id, "The profile_ID was not initialized correctly.")
        self.assertIsNotNone(self.movie_list.movies, "The movies list was not initialized correctly.")


if __name__ == "__main__":
    unittest.main()
