"""Human Activity"""
from enum import Enum

class Activity(Enum):
    """Human activity ID emun."""
    STAND = 0
    SIT = 1
    WALK = 2
    RUN = 3
    WALK_UPSTAIRS = 4
    WALK_DOWNSTAIRS = 5
    LIE = 6
    BIKE = 7
    DRIVE = 8
    RIDE = 9

def get_activity_id(activity_name):
    """Get activity enum from it's name."""
    activity_id = None
    if activity_name == 'STAND':
        activity_id = 0
    elif activity_name == 'SIT':
        activity_id = 1
    elif activity_name == 'WALK':
        activity_id = 2
    elif activity_name == 'RUN':
        activity_id = 3
    elif activity_name == 'WALK_UPSTAIRS':
        activity_id = 4
    elif activity_name == 'WALK_DOWNSTAIRS':
        activity_id = 5
    elif activity_name == 'LIE':
        activity_id = 6
    elif activity_name == 'BIKE':
        activity_id = 7
    elif activity_name == 'DRIVE':
        activity_id = 8
    elif activity_name == 'RIDE':
        activity_id = 9
    else:
        activity_id = 10

    return activity_id
