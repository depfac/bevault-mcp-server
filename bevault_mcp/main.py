import logging
import os

from fastmcp import FastMCP

from .client import BeVaultClient
from .config import Settings
from .logging_config import configure_logging
from .tools import register_all_tools_fastmcp

logger = logging.getLogger(__name__)


def create_mcp_server() -> FastMCP:
    """Create and configure the FastMCP server instance"""
    configure_logging()
    settings = Settings.from_env()

    mcp = FastMCP("bevault-mcp")
    client = BeVaultClient(settings)

    # Register all tools with FastMCP
    register_all_tools_fastmcp(mcp, client)

    # Store client in mcp state for cleanup
    mcp._bevault_client = client

    return mcp


def run() -> None:
    """Run the MCP server with HTTP transport"""
    mcp = create_mcp_server()

    # Get host and port from environment or use defaults
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))

    logger.info("Starting bevault MCP server (HTTP transport) on %s:%s", host, port)
    logger.info("MCP endpoint available at http://%s:%s/mcp", host, port)

    # Run with HTTP transport for n8n compatibility
    mcp.run(transport="http", host=host, port=port)


if __name__ == "__main__":
    run()
