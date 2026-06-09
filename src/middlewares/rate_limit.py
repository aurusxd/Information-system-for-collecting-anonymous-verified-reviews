from time import time
from fastapi import HTTPException, status
from src.core.config import checkRate_MAX_REQUESTS,checkRate_WINDOW_SECONDS
from log import log
requests = {}


def check_rate(ip: str, route: str):
    if not ip:
        return

    now = int(time())
    window_start = now - checkRate_WINDOW_SECONDS
    key = (ip, route)
    history = requests.get(key, [])
    history = [timestamp for timestamp in history if timestamp > window_start]
    history.append(now)
    requests[key] = history

    if len(history) > checkRate_MAX_REQUESTS:
        log.exception("Too many requests, please wait a minute")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests, please wait a minute"
        )
