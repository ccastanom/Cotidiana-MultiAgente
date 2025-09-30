# backend/app/main.py
import time, re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse, Flags
import re
from urllib.parse import quote
from .agents import agente_buscar, agente_analizar, agente_redactar  # ← NUEVO

app = FastAPI(
    title="Cotidiana API",
    description="API de conversación libre. Entrada/salida documentadas. Soporta imagen alusiva por URL.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod restringe a tu dominio/app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Utilidades ---
def detect_pii(q: str) -> bool:
    # demo simple: emails y teléfonos de 7-10 dígitos
    return bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", q) or
                re.search(r"\b\d{7,10}\b", q))

def safe_answer(q: str) -> str:
    """
    Usa tu pipeline multiagente sin tocar su lógica:
    Buscar -> Analizar -> Redactar
    """
    # Guardrail mínimo (no ampliar sobre cosas peligrosas)
    dangerous = ["bomba", "veneno", "sabotear", "dañar", "ilegal"]
    if any(w in q.lower() for w in dangerous):
        return ("No puedo ayudar con actividades peligrosas o ilegales. "
                "Formula otra consulta segura y responsable.")

    # Pipeline multiagente (tu lógica ya existente en backend/app/agents.py)
    tema, texto = agente_buscar(q)
    idea = agente_analizar(texto)
    return agente_redactar(q, idea, tema)

def pick_image_url(q: str) -> str:
    """
    Genera una URL de imagen alusiva usando **toda la frase**.
    """
    clean = re.sub(r"\s+", " ", q.strip())
    tags = clean.replace(" ", ",")
    encoded = quote(tags, safe=",")
    return f"https://source.unsplash.com/800x450/?{encoded}"

# --- Endpoints ---
@app.post("/api/chat", response_model=ChatResponse, summary="Responder consulta libre", tags=["chat"])
def chat_api(req: ChatRequest):
    t0 = time.time()

    # Guardrails mínimos
    pii_found = detect_pii(req.query)

    # Respuesta (multiagente)
    text = safe_answer(req.query)

    # Imagen alusiva
    image_url = pick_image_url(req.query)
    image_alt = f"Imagen alusiva a: {req.query[:60]}"

    ms = (time.time() - t0) * 1000.0
    resp = ChatResponse(
        response=text,
        topic=None,  # si quieres, infiere etiquetas/tema
        executionTime=ms,
        flags=Flags(blocked=False, offtopic=False, pii_in=pii_found, no_data=False),
        timestamp=int(time.time() * 1000),
        image_url=image_url,
        image_alt=image_alt,
    )
    return resp

@app.get("/api/health", summary="Salud del servicio", tags=["meta"])
def health():
    return {"status": "UP", "service": "Cotidiana", "version": "2.0.0"}
