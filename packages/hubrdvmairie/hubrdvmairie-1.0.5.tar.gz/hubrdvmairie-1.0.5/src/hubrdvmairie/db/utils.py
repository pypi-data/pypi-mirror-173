from typing import List

from ..core.config import get_settings
from ..models.editor import Editor
from ..models.municipality import Municipality


def get_all_editors() -> List[Editor]:
    """
    Get global editors from the settings object
    """
    editors_stored: List[Editor] = get_settings().editors_list.copy()
    return editors_stored


def set_all_editors(editors: List[Editor]):
    """
    Set global editors list in the settings object
    """
    get_settings().editors_list = editors


def get_all_meeting_points() -> List[Municipality]:
    """
    Get global meeting point from the settings object
    """
    meeting_point_stored: List[Municipality] = get_settings().meeting_point_list.copy()
    return meeting_point_stored


def set_all_meeting_points(meeting_points: List[Municipality]):
    """
    Set global editors list in the settings object
    """
    get_settings().meeting_point_list = meeting_points
