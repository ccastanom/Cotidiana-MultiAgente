# backend/app/models.py
from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    query: str = Field(..., description="Consulta libre del usuario, sin límite de palabras ni temas.")
    sessionId: Optional[str] = Field(None, description="Identificador opcional de sesión para correlación de logs.")

class Flags(BaseModel):
    blocked: bool = Field(False, description="True si la respuesta fue bloqueada por seguridad.")
    offtopic: bool = Field(False, description="True si la consulta fue fuera de propósito (ya no bloqueamos por esto).")
    pii_in: bool = Field(False, description="Se detectó PII en la consulta.")
    no_data: bool = Field(False, description="No se encontró información suficiente.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Respuesta generada completa (sin límite de palabras).")
    topic: Optional[str] = Field(None, description="Tema inferido o etiqueta libre (opcional).")
    executionTime: float = Field(..., description="Tiempo de generación en milisegundos.")
    flags: Flags = Field(default_factory=Flags, description="Banderas de seguridad.")
    timestamp: int = Field(..., description="Marca de tiempo (epoch ms).")

    # 🔽 NUEVO: soporte de imagen visible para usuarios
    image_url: Optional[str] = Field(None, description="URL de una imagen alusiva a la consulta.")
    image_alt: Optional[str] = Field(None, description="Texto alternativo/leyenda de la imagen.")
