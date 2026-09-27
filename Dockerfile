# syntax=docker/dockerfile:1

# ---------- Stage 1: build do front-end Vue ----------
FROM node:20-slim AS frontend-build

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# ---------- Stage 2: aplicação FastAPI + front-end compilado ----------
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Resultado do build do Vue (stage 1), servido pelo FastAPI em produção
COPY --from=frontend-build /frontend/dist ./frontend/dist

EXPOSE 8000

# Respeita a variável PORT fornecida pelo Render (com fallback para 8000
# em execuções locais via `docker run` sem essa variável definida).
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
