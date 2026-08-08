FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 FOR8KILLO_STATE_PATH=/app/.state
WORKDIR /app
RUN addgroup --system for8killo && adduser --system --ingroup for8killo for8killo
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .
RUN mkdir -p /app/.state && chown -R for8killo:for8killo /app/.state
USER for8killo
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["uvicorn", "foreightkillo.api:app", "--host", "0.0.0.0", "--port", "8000"]
