# backend/app/guardrails.py
import re
from typing import Tuple

BANNED = [
    "fabricar bomba", "bomba", "veneno", "lastimar", "dañar a alguien",
    "sabotear frenos", "arma", "explosivo", "tóxico", "drogas", "ilegal"
]

ALLOWED = [
    "pasta","receta","cocinar","estudio","estudiar","tarea","pomodoro",
    "bici","bicicleta","casco","limpiar","limpieza","cocina","baño","hogar"
]

def moderation_ok(text: str) -> bool:
    low = text.lower()
    return not any(b in low for b in BANNED)

def on_topic(text: str) -> bool:
    low = text.lower()
    return any(w in low for w in ALLOWED)

def pii_mask(text: str) -> Tuple[str, bool]:
    had = False
    new = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[EMAIL_ENMASCARADO]', text)
    if new != text:
        had = True
        text = new
    new = re.sub(r'\b\d{7,15}\b', '[TEL_ENMASCARADO]', text)
    if new != text:
        had = True
        text = new
    return text, had

def limitar_palabras(text: str, max_words: int = 40) -> str:
    words = text.strip().split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + " …"
