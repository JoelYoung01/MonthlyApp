FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# The build context is this directory, which is also the `api` Python package.
COPY __init__.py main.py /app/api/
COPY core /app/api/core
COPY models /app/api/models
COPY routes /app/api/routes
COPY schemas /app/api/schemas
COPY dist /app/dist

RUN mkdir -p /app/api/data
VOLUME /app/api/data

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
