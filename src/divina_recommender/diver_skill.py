from enum import IntEnum

class DiverSkill(IntEnum):
    """
    Enum representing diver's skills mapped to difficulty levels 1-4.
    """
    FIRST_TIME = 1
    OPEN_WATER = 2
    ADVANCED_OPEN_WATER = 3
    TECHNICAL_DIVER = 4
