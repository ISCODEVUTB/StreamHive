from enum import Enum

class ProfileRoles(str, Enum):
    """
    Enum representing the different roles a user profile can have.

    Attributes:
        SUBSCRIBER: A regular user.
        CRITIC: A verified user with higher influence. Their reviews carry
                more weight and visibility.
        EDITOR: A user with writes content for the newspaper (writes articles).
    """
    SUBSCRIBER = 'subscriber'
    CRITIC = 'critic'
    EDITOR = 'editor'