# 🤖 Cotidiana – Agente Conversacional Multiagente

Cotidiana es un agente conversacional diseñado como **solución agéntica académica**.  
Su objetivo es dar consejos prácticos y seguros de la vida diaria en cuatro temas:

1. 🍝 Cocinar pasta  
2. 📚 Técnicas de estudio (ej. Pomodoro)  
3. 🚲 Uso seguro de la bicicleta  
4. 🧽 Limpieza del hogar  

---

## ✨ Características

- **Arquitectura multiagente**: Buscar → Analizar → Redactar  
- **Guardrails**:
  - Bloqueo de palabras prohibidas (ej: “arma”, “sabotear frenos”)  
  - Solo responde en temas permitidos  
  - Enmascara datos sensibles (emails, teléfonos)  
  - Limita la salida a 40 palabras  
- **Registro de logs**: Cada consulta queda registrada con tiempo y banderas de seguridad.

---

## ⚖️ Principios Éticos

- **Privacidad**: No se almacenan ni procesan datos sensibles sin consentimiento.  
- **Responsabilidad**: Rechaza cualquier solicitud peligrosa, ilegal o dañina.  
- **Conciencia de límites**: Solo responde sobre pasta, estudio, bicicleta y limpieza.  
- **Claridad y transparencia**: Respuestas breves, con fuente citada.  

---

## 🚀 Despliegue

- **Local**:
  ```bash
  python src/main.py
  
# Backend - Cotidiana (FastAPI)

Instalación:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Ejecutar:
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

Endpoints:
GET /api/health
POST /api/chat  { "query": "...", "sessionId": "..." }
GET  /api/logs
