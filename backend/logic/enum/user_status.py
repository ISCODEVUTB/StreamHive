from enum import Enum

class UserStatus(str, Enum):
    """
    Enum class that represents the possible statuses of a user in the system.

    Attributes:
        ACTIVE: Represents an active user.
        INACTIVE: Represents a user who is inactive.
        DELETED: Represents a user who has been deleted.

    The `UserStatus` enum is used to categorize the state of a user account,
    allowing for a predefined set of valid user statuses.
    """

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'