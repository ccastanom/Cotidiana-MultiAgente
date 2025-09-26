# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from .agents import agente_buscar, agente_analizar, agente_redactar
from .guardrails import moderation_ok, on_topic, pii_mask, limitar_palabras
from .logs import append_log, get_logs
from .models import ChatRequest, ChatResponse

app = FastAPI(title="Cotidiana - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringir en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "UP", "service": "Cotidiana", "version": "1.0.0"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    t0 = time.time()
    q_original = req.query
    flags = {"blocked": False, "offtopic": False, "pii_in": False, "no_data": False}

    if not moderation_ok(q_original):
        flags["blocked"] = True
        ms = int((time.time() - t0) * 1000)
        append_log({"query": q_original, "flags": flags, "ms": ms})
        return ChatResponse(response="❌ Bloqueado por seguridad.", topic=None, executionTime=ms, flags=flags, timestamp=int(time.time()*1000))

    if not on_topic(q_original):
        flags["offtopic"] = True
        ms = int((time.time() - t0) * 1000)
        append_log({"query": q_original, "flags": flags, "ms": ms})
        return ChatResponse(response="⚠️ Tema fuera de alcance. Usa: cocinar pasta, estudiar, bici o limpieza.", topic=None, executionTime=ms, flags=flags, timestamp=int(time.time()*1000))

    q_safe, had_pii = pii_mask(q_original)
    flags["pii_in"] = had_pii

    tema, texto = agente_buscar(q_safe)
    if tema is None or texto is None:
        flags["no_data"] = True
        resp_text = "No tengo suficiente información en mi CORPUS para esa pregunta."
    else:
        idea = agente_analizar(texto)
        if idea is None:
            flags["no_data"] = True
            resp_text = "No tengo suficiente información en mi CORPUS para esa pregunta."
        else:
            resp_text = agente_redactar(q_safe, idea, tema)

    resp_text = limitar_palabras(resp_text, 40)
    resp_text, _ = pii_mask(resp_text)

    ms = int((time.time() - t0) * 1000)
    append_log({"query": q_original, "flags": flags, "ms": ms})
    return ChatResponse(response=resp_text, topic=tema, executionTime=ms, flags=flags, timestamp=int(time.time()*1000))

@app.get("/api/logs")
def logs(limit: int = 100):
    return get_logs(limit)
