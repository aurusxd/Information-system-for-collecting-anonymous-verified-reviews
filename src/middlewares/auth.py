from fastapi import status
from log import log

def validate_owner_token(token: str, box):
    if not token or token != box.owner_token:
        log.exception(f"Invalid owner token {status.HTTP_403_FORBIDDEN}")
        raise