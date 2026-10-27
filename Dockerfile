FROM node:22-alpine AS ui
WORKDIR /frontend
COPY web/package.json ./
RUN npm install --no-audit --no-fund
COPY web/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY agenqo/ agenqo/
COPY --from=ui /frontend/dist/ /app/web_dist/
RUN pip install --no-cache-dir .
RUN useradd -r -u 10001 agenqo
USER agenqo
EXPOSE 8080
CMD ["uvicorn", "agenqo.api:app", "--host", "0.0.0.0", "--port", "8080"]
