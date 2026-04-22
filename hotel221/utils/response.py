from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    message: str
    timestamp: str
    data: Optional[Any] = None


def send_response(message: str, data: Any = None, success: bool = True) -> dict:
    """Formate toutes les réponses de l'API de manière uniforme."""
    return {
        "success": success,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }
