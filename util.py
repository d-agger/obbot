import math
from typing import Tuple

from pycountry.db import Country


def is_mention(string: str | None) -> bool:
    try:
        if string is None:
            return False
        return string.startswith("<@") and string.endswith(">")
    except Exception:
        return False

def id_from_mention(ping: str | None) -> int | None:
    try:
        if ping is None:
            return None
        return int(ping.strip("<@\u200b>"))
    except Exception:
        return None

def mention(user_id: str | int) -> str:
    try:
        return f"<@{user_id}>"
    except Exception:
        return f"<broken ping>"

def fancy_country_string(c_obj: Country | None) -> str | None:
    if c_obj is None:
        return None
    return f"{c_obj.flag}` {c_obj.name} ({c_obj.alpha_3})`"

def m_to_ft(meters: float) -> Tuple[int, int]:
    total_inches = meters * 100 / 2.54
    feet: int = int(total_inches // 12)
    inches: int = math.ceil(total_inches % 12)
    return feet, inches

def ft_to_m(feet: int, inches: int) -> float:
    return (feet * 12 + inches) * 2.54 / 100.0