FROM python:3.11-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl build-essential libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Crear directorio
WORKDIR /app

# Copiar pyproject.toml y poetry.lock primero (para cacheo de capas)
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias
RUN poetry install --no-root

# Copiar el código
COPY . .

EXPOSE 8000
