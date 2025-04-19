FROM python:3.11-slim AS base

WORKDIR /app
RUN pip install --no-cache-dir poetry

FROM base AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry config installer.parallel false && \
    poetry install --no-root

FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY cloud_run cloud_run/
COPY static static/
COPY templates templates/

EXPOSE 8000
CMD ["uvicorn", "cloud_run.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
