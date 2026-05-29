FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY scripts/ ./scripts

ENTRYPOINT ["uv", "run", "python", "scripts/ingest_data_args.py"]