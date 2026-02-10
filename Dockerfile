# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install runtime deps first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Default environment variables (override via .env or docker run -e)
ENV REQUEST_TIMEOUT_SECONDS=30

# Run the MCP server via module
CMD ["python", "-m", "bevault_mcp.main"]
