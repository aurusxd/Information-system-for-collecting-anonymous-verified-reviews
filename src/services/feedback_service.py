from src.models.feedback import Feedback
from src.utils.validators import moderate_text
from fastapi import HTTPException, status
from log import log

def create_feedback(db, box_id, text):
    try:
        text = moderate_text(text)
    except ValueError as e:
        log.exception(f"Error: {e}, status: {status.HTTP_400_BAD_REQUEST}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    fb = Feedback(box_id=box_id, text=text, status="approved")
    db.add(fb)
    db.commit()
    db.refresh(fb)
    log.info("Feedback created")
    return fb