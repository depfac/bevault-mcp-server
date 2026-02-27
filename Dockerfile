# syntax=docker/dockerfile:1
FROM python:3.13-slim

LABEL org.opencontainers.image.title="bevault-mcp"
LABEL org.opencontainers.image.description="MCP (Model Context Protocol) server for beVault - tools to interact with beVault's API for Build, Source, and Distribute modules"
LABEL org.opencontainers.image.source="https://github.com/depfac/bevault-mcp-server"
LABEL org.opencontainers.image.url="https://github.com/depfac/bevault-mcp-server"
LABEL org.opencontainers.image.documentation="https://support.bevault.io/en/bevault-documentation/current-version/bevault-mcp-server"
LABEL org.opencontainers.image.vendor="Deployments Factory"
LABEL org.opencontainers.image.licenses="MIT"

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
