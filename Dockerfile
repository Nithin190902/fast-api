# 1. Base image: pick the Python your project already runs on.
#    "slim" strips docs/compilers you don't need -> much smaller image.
FROM python:3.14-slim

# 2. Sensible Python defaults inside containers:
#    - don't write .pyc files (no benefit in a throwaway container)
#    - flush stdout immediately so `docker logs` shows output live
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Everything after this runs from /app inside the container.
WORKDIR /app

# 4. Copy ONLY requirements first, then install.
#    Docker caches each layer. If your code changes but requirements.txt
#    doesn't, this expensive step is skipped on the next build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now copy the actual source. This layer changes often, so it goes last.
COPY . .

# 6. Documentation only: tells readers (and compose) which port the app uses.
EXPOSE 8000

# 7. The command that runs when the container starts.
#    --host 0.0.0.0 is REQUIRED: 127.0.0.1 would only be reachable from
#    inside the container, not from your Mac.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
