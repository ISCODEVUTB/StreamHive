from enum import Enum

class UserTypes(str, Enum):
    """
    Enum class that represents the different types of users in the system.

    Attributes:
        INTERNAL: Represents a user who is part of the internal organization or system.
        EXTERNAL: Represents a user who is external to the organization or system.
        ADMIN: Represents a user who can administrate the whole system.

    The `UserTypes` enum is used to differentiate between internal, external, and admin users, 
    categorizing them for appropriate access or functionality.
    """
    
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    ADMIN = 'admin'