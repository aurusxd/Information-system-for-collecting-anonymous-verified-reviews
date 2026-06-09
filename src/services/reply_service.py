from src.models.reply import Reply
from src.utils.validators import moderate_text
from fastapi import HTTPException, status
from log import log


def create_reply(db, feedback_id, text):
    try:
        text = moderate_text(text)
    except ValueError as e:
        log.exception(f"Error: {e}, status: {status.HTTP_400_BAD_REQUEST}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    reply = Reply(feedback_id=feedback_id, text=text)
    db.add(reply)
    db.commit()
    db.refresh(reply)
    log.info("Reply created")
    return reply