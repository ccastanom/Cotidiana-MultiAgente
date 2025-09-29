# backend/app/main.py (fragmento)
import time, re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse, Flags
import re
from urllib.parse import quote

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

# --- Utilidades muy simples (placeholder) ---
def detect_pii(q: str) -> bool:
    # demo simple: emails y teléfonos de 7-10 dígitos
    return bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", q) or
                re.search(r"\b\d{7,10}\b", q))

def safe_answer(q: str) -> str:
    """
    Aquí conectas tu pipeline real (multiagente).
    Este demo solo devuelve el texto “tal cual” + un tip básico.
    IMPORTANTE: mantén tus guardrails para rechazar contenido ilegal/dañino.
    """
    # Ejemplo de bloqueo mínimo (NO ampliar sobre cosas peligrosas)
    dangerous = ["bomba", "veneno", "sabotear", "dañar", "ilegal"]
    if any(w in q.lower() for w in dangerous):
        return ("No puedo ayudar con actividades peligrosas o ilegales. "
                "Formula otra consulta segura y responsable.")

    # Sin límite de palabras: devuelve respuesta amplia
    return f"Respuesta generada sobre: {q}. (Ejemplo demo; integra aquí tu lógica multiagente)."

def pick_image_url(q: str) -> str:
    """
    Genera una URL de imagen alusiva usando **toda la frase**.
    - No limitamos la cantidad de palabras.
    - Sanitizamos solo para compatibilidad de URL.
    - Pasamos la frase completa a Unsplash Source.
    - Fallback a Picsum si quisieras (descomenta la última línea).
    """
    # 1) Normaliza espacios y quita solo caracteres que rompen URL (sin perder significado)
    #    NOTA: no truncamos la frase; preservamos su semántica completa.
    clean = re.sub(r"\s+", " ", q.strip())
    # 2) Unsplash funciona mejor con separadores de coma. Reemplazamos espacios por comas.
    tags = clean.replace(" ", ",")
    # 3) Codificamos la frase entera
    encoded = quote(tags, safe=",")  # comas sin codificar; resto URL-encoded

    # Unsplash Source con tamaño fijo (mejor para Streamlit)
    return f"https://source.unsplash.com/800x450/?{encoded}"

    # Si prefieres un fallback que siempre devuelve algo (aunque no sea semántico):
    # from urllib.parse import quote_plus
    # seed = quote_plus(q)
    # return f"https://picsum.photos/seed/{seed}/800/450"


# --- Endpoints ---
@app.post("/api/chat", response_model=ChatResponse, summary="Responder consulta libre", tags=["chat"])
def chat_api(req: ChatRequest):
    t0 = time.time()

    # Guardrails mínimos
    pii_found = detect_pii(req.query)

    # Respuesta sin límite de palabras
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
