FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt -r requirements-dev.txt

FROM python:3.11-slim AS runtime
WORKDIR /app

ARG UID=10001
ARG GID=10001
ARG APP_USER=appuser

RUN groupadd -r ${APP_USER} -g ${GID} && \
    useradd -r -u ${UID} -g ${APP_USER} ${APP_USER} && \
    apt-get update && apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /root/.local /home/${APP_USER}/.local
COPY --chown=${APP_USER}:${APP_USER} . .

RUN chown -R ${APP_USER}:${APP_USER} /app && \
    chmod -R 755 /home/${APP_USER} && \
    find /home/${APP_USER}/.local -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /app -name "*.pyc" -delete

USER ${APP_USER}
ENV PATH="/home/${APP_USER}/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]