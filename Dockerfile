FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY agenqo/ agenqo/
RUN pip install --no-cache-dir .
RUN useradd -r -u 10001 agenqo
USER agenqo
EXPOSE 8080
CMD ["uvicorn", "agenqo.api:app", "--host", "0.0.0.0", "--port", "8080"]
