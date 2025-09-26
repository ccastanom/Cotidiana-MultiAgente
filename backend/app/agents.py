# backend/app/agents.py
# Agentes: Buscar -> Analizar -> Redactar
import re
from typing import Tuple, Optional

CORPUS = {
    "pasta": "Para una pasta sencilla: hervir agua con sal, cocinar 8–10 min; saltear ajo en aceite, agregar tomate y sal; mezclar con un poco de agua de cocción.",
    "estudio": "Usa Pomodoro: 25 min de foco + 5 de descanso. Haz lista de 3 tareas máximas y empieza por la más corta.",
    "bicicleta": "Antes de salir en bici: revisa frenos y llantas, lleva agua, luces si es de noche y usa casco.",
    "limpieza": "Para grasa ligera en cocina: mezcla agua + vinagre. Para manchas pegadas: bicarbonato con un poco de agua."
}

def agente_buscar(pregunta: str) -> Tuple[Optional[str], Optional[str]]:
    q = pregunta.lower()
    if any(w in q for w in ["pasta", "receta", "cocinar"]):
        return "pasta", CORPUS["pasta"]
    if any(w in q for w in ["estudio", "estudiar", "tarea", "pomodoro"]):
        return "estudio", CORPUS["estudio"]
    if any(w in q for w in ["bici", "bicicleta", "casco", "salir"]):
        return "bicicleta", CORPUS["bicicleta"]
    if any(w in q for w in ["limpiar", "limpieza", "cocina", "baño", "hogar"]):
        return "limpieza", CORPUS["limpieza"]
    return None, None

def agente_analizar(texto: Optional[str]) -> Optional[str]:
    if texto is None or texto == "SIN_RESULTADOS":
        return None
    parts = re.split(r'[.!?]', texto)
    idea = parts[0].strip() if parts else None
    return idea or None

def agente_redactar(pregunta: str, idea: Optional[str], tema: Optional[str]) -> str:
    if idea is None:
        return "No tengo suficiente información para responder."
    # Formato conciso: idea + fuente
    return f"{idea} | Fuente: {tema}"
