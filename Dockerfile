# ---------- Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy application source
COPY . .

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# ---------- Runtime ----------
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r app \
    && useradd -r -g app -m -d /home/app app

WORKDIR /app

# Copy application and virtual environment
COPY --from=builder /app /app

# Use project's virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Hugging Face cache
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV SENTENCE_TRANSFORMERS_HOME=/app/.cache/huggingface

# Create required directories and entrypoint
RUN mkdir -p \
    /app/.cache/huggingface \
    /app/data/chroma_db \
    /app/storage/images \
    && printf '#!/bin/sh\nset -e\nalembic upgrade head\nexec "$@"\n' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh \
    && chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]