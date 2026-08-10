FROM python:3.11-slim

RUN groupadd -r app && useradd -r -m -d /home/app -g app app

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .
ENV PATH="/app/.venv/bin:$PATH"
ENV HOME=/home/app
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN chown -R app:app /app /home/app
USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0"]