from enum import Enum

class TargetTypes(str, Enum):
    """
    Enum class that defines the types of targets that actions or references 
    can be associated with.

    Attributes:
        MOVIE: Represents a target of type 'movie'.
        COMMENT: Represents a target of type 'comment'.
        ARTICLE: Represents a target of type 'article'.

    This enum is useful for scenarios where various entities (like likes, reports, 
    or references) need to be associated with different content types.
    """
    
    MOVIE = 'movie'
    COMMENT = 'comment'
    ARTICLE = 'article'