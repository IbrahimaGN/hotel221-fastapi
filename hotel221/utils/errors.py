from fastapi import HTTPException


def not_found(resource: str, id: int):
    """Lève une erreur 404 standardisée."""
    raise HTTPException(status_code=404, detail=f"{resource} avec l'id {id} introuvable")


def conflict(message: str):
    """Lève une erreur 409 Conflict."""
    raise HTTPException(status_code=409, detail=message)


def bad_request(message: str):
    """Lève une erreur 400 Bad Request."""
    raise HTTPException(status_code=400, detail=message)
