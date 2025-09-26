# Despliegue de Cotidiana

## Local
```bash
cd backend
uvicorn app.main:app --reload --port 8080

cd frontend
npm install
npm run dev
