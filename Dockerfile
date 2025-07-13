FROM python:3.13-slim AS base

RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

FROM base AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY data/ ./data/

COPY app/ ./app/
