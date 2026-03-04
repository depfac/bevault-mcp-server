import logging
import os
from pathlib import Path

import uvicorn
from fastmcp import FastMCP
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.utilities.types import Image
from mcp.types import Icon
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .client import BeVaultClient
from .config import Settings
from .logging_config import configure_logging
from .sentry_config import init_sentry
from .tools import register_all_tools_fastmcp

logger = logging.getLogger(__name__)


def create_mcp_server() -> FastMCP:
    """Create and configure the FastMCP server instance"""
    configure_logging()
    settings = Settings.from_env()

    oidc_config = settings.get_oidc_config()
    auth = None
    if oidc_config is not None:
        oidc_kwargs: dict={
            "config_url": oidc_config.config_url,
            "client_id": oidc_config.client_id,
            "client_secret": oidc_config.client_secret,
            "base_url": oidc_config.base_url,
        }
        if oidc_config.audience is not None:
            oidc_kwargs["audience"] = oidc_config.audience
        if oidc_config.redirect_path is not None:
            oidc_kwargs["redirect_path"] = oidc_config.redirect_path
        if oidc_config.required_scopes is not None:
            oidc_kwargs["required_scopes"] = oidc_config.required_scopes
        auth = OIDCProxy(**oidc_kwargs)
        logger.info("OIDC authentication enabled")
    else:
        logger.info("Authentication mode: bevault-api-key header (OIDC not configured)")


    icon_path = Path(__file__).resolve().parent / "assets" / "badge-color.svg"
    icon = Icon(
        src=Image(path=str(icon_path)).to_data_uri(),
        mimeType="image/svg+xml",
        sizes=["48x48"],
    )
    mcp_kwargs: dict={
        "website_url": "https://github.com/depfac/bevault-mcp-server",
        "icons": [icon],
    }
    if auth is not None:
        mcp_kwargs["auth"] = auth

    mcp = FastMCP("bevault-mcp",**mcp_kwargs)
    client = BeVaultClient(settings)

    # Register all tools with FastMCP
    register_all_tools_fastmcp(mcp, client)

    # Store client in mcp state for cleanup
    mcp._bevault_client = client

    return mcp


def run() -> None:
    """Run the MCP server with HTTP transport"""
    init_sentry()
    mcp = create_mcp_server()

    # CORS middleware required for OIDC authentication with Browser-based clients (https://gofastmcp.com/deployment/http#cors-for-browser-based-clients)
    cors_origins_raw = os.getenv("CORS_ORIGINS", "").strip()
    if cors_origins_raw:
        allow_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
        if allow_origins:
            middleware = [
                Middleware(
                    CORSMiddleware,
                    allow_origins=allow_origins,
                    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
                    allow_headers=[
                        "mcp-protocol-version",
                        "mcp-session-id",
                        "Authorization",
                        "Content-Type",
                        "bevault-api-key",
                    ],
                    expose_headers=["mcp-session-id"],
                )
            ]
            app = mcp.http_app(middleware=middleware)
            logger.info("CORS enabled for origins: %s", allow_origins)
        else:
            app = mcp.http_app()
    else:
        app = mcp.http_app()

    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))

    logger.info("Starting bevault MCP server (HTTP transport) on %s:%s", host, port)
    logger.info("MCP endpoint available at http://%s:%s/mcp", host, port)

    # Run with HTTP transport for n8n compatibility
    mcp.run(transport="http", host=host, port=port)


if __name__ == "__main__":
    run()
