# Arquitectura de Cotidiana

El sistema está dividido en:
- **Frontend** (React+Vite+TS): interfaz del usuario.
- **Backend** (FastAPI): lógica de agentes, guardrails y logs.
- **Documentación**: guías técnicas, ética y despliegue.

```mermaid
flowchart LR
U[Usuario] -->|consulta| FE[Frontend]
FE -->|HTTP/JSON| BE[Backend]
BE --> Agentes --> Corpus
