from typing import Any


def to_bool(val: Any) -> bool:
    """ Cast any value into boolean """
    return not (not val or val in ("False", "None"))
