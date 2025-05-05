from enum import Enum

class UserGender(str, Enum):
    """
    Enum class that represents the possible genders of a user in the system.

    Attributes:
        MALE: Represents user who persives themself as male.
        FEMALE: Represents user who persives themself as female.
        OTHER: Represents user who persives themself as an other gender.

    The `UserGender` enum is used to categorize the gender of a user, allowing for a 
    predefined set of valid user genders.
    """

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'