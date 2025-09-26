# backend/app/models.py
from pydantic import BaseModel
from typing import Optional, Dict

class ChatRequest(BaseModel):
    query: str
    sessionId: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    topic: Optional[str]
    executionTime: int
    flags: Dict[str, bool]
    timestamp: int
