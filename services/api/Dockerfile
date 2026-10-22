FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.lock requirements-dev.lock ./
RUN pip install --no-cache-dir --require-hashes -r requirements.lock
ENV PYTHONPATH=/app
COPY pyproject.toml ./
COPY app ./app
COPY data ./data
COPY migrations ./migrations
COPY alembic.ini ./
RUN useradd --create-home --uid 10001 nour
USER nour
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-proxy-headers"]

FROM base AS test
USER root
RUN pip install --no-cache-dir --require-hashes -r requirements-dev.lock
COPY tests ./tests
USER nour
CMD ["pytest", "-q"]
