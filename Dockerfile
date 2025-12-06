# Basis-Image: Leichtgewichtiges Python
FROM python:3.11-slim

# Metadaten
LABEL maintainer="Sebastian Noschka"
LABEL description="Cannaleo Support Agent Service"

# Environment Variablen setzen (Python Output unbuffered für bessere Logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Arbeitsverzeichnis im Container
WORKDIR /app

# Dependencies installieren (Caching nutzen!)
# Wir kopieren erst nur die requirements, damit Docker den Cache nutzen kann,
# wenn sich nur der Code ändert, aber nicht die Libs.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source Code kopieren
COPY src/ ./src/

# Port exponieren (Doku-Zweck)
EXPOSE 8000

# Start-Befehl (wird meist von docker-compose überschrieben, aber gut als Fallback)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]