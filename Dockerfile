FROM python:3.14.7-slim


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


ENV UV_COMPILE_BYTECODE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY pyproject.toml uv.lock ./


RUN uv sync --frozen --no-install-project --all-groups


COPY src/ ./src


RUN uv sync --frozen --all-groups


