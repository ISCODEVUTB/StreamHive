from enum import Enum

class InteractTypes(str, Enum):
    """
    Enum class that defines the types of interactions users can perform.

    Attributes:
        LIKED: Represents a 'like' interaction with a target.
        COMMENT: Represents a 'comment' interaction with a target.

    This enum can be used to categorize user interactions with content, such as 
    tracking or filtering actions like likes and comments.
    """

    LIKED = 'liked'
    COMMENT = 'comment'