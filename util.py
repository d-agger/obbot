def is_ping(string: str | None) -> bool:
    try:
        if string is None:
            return False
        return string.startswith("<@") and string.endswith(">")
    except Exception:
        return False

def id_from_ping(ping: str | None) -> int | None:
    try:
        if ping is None:
            return None
        return int(ping.strip("<@\u200b>"))
    except Exception:
        return None

def ping_id(user_id: str) -> str:
    try:
        return f"<@{user_id}>"
    except Exception:
        return f"<broken ping>"