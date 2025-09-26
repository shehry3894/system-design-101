# Base Python image
FROM python:3.11-slim AS base

# Prevent Python from creating .pyc files (saves space).
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure logs are written directly to stdout/stderr (important for Docker logging).
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /usr/src/app

# Install uv (very small, just a single binary)
RUN pip install --no-cache-dir uv

# Copy project files
COPY uv.lock pyproject.toml ./

# Cache uv dependencies between builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-cache

# Copy application code
COPY ./app /usr/src/app

RUN echo ls

ENV PYTHONPATH=/usr/src

# Expose port for uvicorn
EXPOSE 8000

# Default command to run the app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
