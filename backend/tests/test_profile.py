import unittest
from datetime import datetime
from backend.logic.entities.profile import Profile
from backend.logic.entities.profile_roles import ProfileRoles


class TestProfile(unittest.TestCase):
    """
    Test cases for the Profile class.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a sample Profile object.
        """
        self.profile = Profile(
            username="johndoemovies",
            description="Lover of horror and romance movies.",
            profile_pic_url="https://example.com/profile_pic.png",
            profile_role=ProfileRoles.SUBSCRIBER
        )

    def test_profile_init(self):
        """
        Test the initialization of the Profile object.
        """
        self.assertIsNotNone(self.profile.profile_id, "Profile ID should not be None.")
        self.assertIsNotNone(self.profile.created_at, "Created at timestamp should not be None.")
        self.assertEqual(self.profile.username, "johndoemovies", "Username was not initialized correctly.")
        self.assertEqual(self.profile.description, "Lover of horror and romance movies.", "Description was not initialized correctly.")
        self.assertEqual(self.profile.profile_pic_url, "https://example.com/profile_pic.png", "Profile picture URL was not initialized correctly.")
        self.assertEqual(self.profile.profile_role, ProfileRoles.SUBSCRIBER, "Profile role was not initialized correctly.")
        self.assertEqual(self.profile.movie_lists_count, 2, "Movie lists count should start at 2.")
        self.assertEqual(self.profile.follower_count, 0, "Follower count should start at 0.")
        self.assertEqual(self.profile.follow_count, 0, "Follow count should start at 0.")
        self.assertEqual(self.profile.movies_rated_count, 0, "Movies rated count should start at 0.")
        self.assertEqual(self.profile.comments_count, 0, "Comments count should start at 0.")
        self.assertIsNotNone(datetime.fromisoformat(self.profile.created_at), "Created_at is not a valid ISO datetime.")

    def test_setters(self):
        """
        Verify the setters update the correct attributes.
        """
        self.profile.username = "janedoecritic"
        self.profile.description = "Love reviewing movies."
        self.profile.profile_pic_url = "https://example.com/new_pic.png"
        self.profile.profile_role = ProfileRoles.CRITIC

        self.assertEqual(self.profile.username, "janedoecritic")
        self.assertEqual(self.profile.description, "Love reviewing movies.")
        self.assertEqual(self.profile.profile_pic_url, "https://example.com/new_pic.png")
        self.assertEqual(self.profile.profile_role, ProfileRoles.CRITIC)

    def test_description_length_validation(self):
        """
        Ensure that a ValueError is raised if description exceeds max allowed length.
        """
        long_description = "x" * (Profile.MAX_DESCRIPTION_LENGTH + 1)
        with self.assertRaises(ValueError, msg="A ValueError should be raised for exceeding max description length."):
            self.profile.description = long_description

    def test_increment_methods(self):
        """
        Test all increment methods increase their respective counters by one.
        """
        self.profile.increment_movie_lists_count()
        self.profile.increment_follower_count()
        self.profile.increment_follow_count()
        self.profile.increment_movies_rated_count()
        self.profile.increment_comments_count()

        self.assertEqual(self.profile.movie_lists_count, 3, "Movie list count should be incremented.")
        self.assertEqual(self.profile.follower_count, 1, "Follower count should be incremented.")
        self.assertEqual(self.profile.follow_count, 1, "Follow count should be incremented.")
        self.assertEqual(self.profile.movies_rated_count, 1, "Movies rated count should be incremented.")
        self.assertEqual(self.profile.comments_count, 1, "Comments count should be incremented.")

    def test_str_representation(self):
        """
        Test the __str__ method returns a string with key profile information.
        """
        profile_str = str(self.profile)
        self.assertIn("profile_id", profile_str)
        self.assertIn("username", profile_str)
        self.assertIn("profile_role", profile_str)
        self.assertIn("comments_count", profile_str)
        self.assertIn("movie_lists_count", profile_str)


if __name__ == '__main__':
    unittest.main()
