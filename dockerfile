# Stage 1: Builder
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# Install dependencies (cached layer)
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy code and sync project
COPY . .
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.11-slim-bookworm
WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the pre-built venv and code
COPY --from=builder --chown=appuser:appuser /app /app

# Point to the venv
ENV PATH="/app/.venv/bin:$PATH"

USER appuser
EXPOSE 8000

# FIX: Run uvicorn directly instead of 'uv run'
# This avoids runtime permission checks by the uv binary
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Replace your current uvicorn command with this
CMD ["gunicorn", "-w", "8", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]
