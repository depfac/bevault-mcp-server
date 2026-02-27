# bevault-mcp

## Introduction

This is the MCP (Model Context Protocol) server for [beVault](https://www.bevault.io/), a modern data platform designed to manage scalable, secure, and auditable data using Data Vault methodology.

This MCP server allows you to perform actions that users can do in the following beVault modules:
- **Build**: Create and manage data models (Hubs, Links, Satellites, Reference Tables)
- **Source**: Manage source systems, data packages, and staging tables
- **Distribute**: Create and manage information marts and their scripts

> **Note**: Support for the **Verify** module will be added in a future release.

> **v1.1.0 Migration**: With version v1.1.0 of this project, we migrated to FastMCP v3 which no longer supports the `Authorization` header to pass the beVault API token. As of v1.1.0, make sure to use the new `bevault-api-key` header in your MCP client to pass your beVault API token.

The server exposes tools to interact with beVault's API using FastMCP with HTTP transport.

## Features
- `search_model`: search entities (Hubs, Links, Satellites, ReferenceTables) in a beVault project
- `search_information_marts`: search and list information marts (with simplified script info)
- `get_information_mart_script`: retrieve full information mart script definition (metadata + columns + sources)
- `search_source_systems`: search source systems and their data packages (with staging table info)
- `create_*` / `update_*` / `delete_*` tools for hubs, links, source systems, data packages, information marts and scripts
- `create_staging_table` and column tools to define and evolve staging tables
- Mapping tools (`map_column_to_hub`, `map_columns_to_link`, `map_columns_to_satellite`, delete/update mapping helpers)
- Introspection tools like `get_link`, `get_satellite`, `get_staging_table`, `get_snapshots`

## Installation

### Development Setup

For development, you can set up the project locally:

1. **Download the code** from the repository
2. **Install Python** (Python >= 3.13 required)
3. **Install dependencies** from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```



### Production Setup

For production, you can use Docker and docker-compose. The project uses our own registry:

**Docker Image**: `quay.io/dfakto_org/bevault_mcp`

You can pull and run the image directly:
```bash
docker pull quay.io/dfakto_org/bevault_mcp
docker run -e BEVAULT_BASE_URL=<your-url> -e REQUEST_TIMEOUT_SECONDS=30 quay.io/dfakto_org/bevault_mcp
```

**Quick deployment with Docker Compose**

Create a `docker-compose.yml` file:

```yaml
services:
  bevault-mcp:
    container_name: bevault-mcp
    image: quay.io/dfakto_org/bevault_mcp:v1.0.0
    environment:
      BEVAULT_BASE_URL: "https://bevault.your.domain"
      REQUEST_TIMEOUT_SECONDS: "30"
      MCP_HOST: 0.0.0.0
      MCP_PORT: "8000"
    ports:
      - "8000:8000"
    restart: always
```

Then run:
```bash
docker compose up -d
```

The MCP server will be available at `http://localhost:8000/mcp`. Remember to replace `https://bevault.your.domain` with your actual beVault instance URL.

> **Deploying alongside beVault**: If you run the MCP server in the same docker-compose stack as beVault (see [Production deployment](https://support.bevault.io/en/bevault-documentation/current-version/architecture-installation/deployment/production-deployment)), you can set `BEVAULT_BASE_URL` to the **metavault-ui** service name instead of an external URL (e.g. `http://metavault-ui:80`). This is required because the MCP tools call the `/metavault` routes, which are served by the embedded reverse proxy of the metavault-ui front-end application.

## Configuration

### Environment Variables

The following environment variables are required to run the MCP server:

Create a `.env` file in the project root or set these environment variables:

```ini
BEVAULT_BASE_URL=https://bevault.metavault.url.com
REQUEST_TIMEOUT_SECONDS=30
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

**Required Variables:**
- `BEVAULT_BASE_URL`: The URL of your beVault MetaVault instance (required)
- `REQUEST_TIMEOUT_SECONDS`: Number of seconds after which requests to beVault's API will timeout (required)

**Optional Variables:**
- `MCP_HOST`: The host address on which the MCP server will run (optional, default: `0.0.0.0`)
- `MCP_PORT`: The port on which the MCP server will run (optional, default: `8000`)

### Sentry Monitoring

Sentry integration is optional. When `SENTRY_DSN` is set, the server initializes Sentry with the [MCP integration](https://docs.sentry.io/platforms/python/integrations/mcp/) for monitoring tool executions, errors, and performance.

```ini
# Sentry (optional - unset or leave empty to disable)
SENTRY_DSN=https://your-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_SEND_DEFAULT_PII=false
SENTRY_SERVER_NAME=bevault-mcp-prod
SENTRY_DEFAULTTAGS__service=bevault-mcp
SENTRY_DEFAULTTAGS__deployment=prod
```

| Variable | Default | Description |
|----------|---------|-------------|
| `SENTRY_DSN` | — | Sentry project DSN; required to enable Sentry |
| `SENTRY_ENVIRONMENT` | `production` | Environment name for grouping in Sentry |
| `SENTRY_TRACES_SAMPLE_RATE` | `1.0` | Fraction of transactions to trace (0.0–1.0) |
| `SENTRY_SEND_DEFAULT_PII` | `false` | Include tool inputs/outputs (PII) in events |
| `SENTRY_DEBUG` | `false` | Enable Sentry SDK debug logging |
| `SENTRY_INCLUDE_PROMPTS` | `true` | Include prompt/tool data in spans (when PII enabled) |
| `SENTRY_SERVER_NAME` | — | Server instance identifier |
| `SENTRY_DEFAULTTAGS__[key]` | — | Default tags, e.g. `SENTRY_DEFAULTTAGS__service=bevault-mcp` |

### Authentication

Authentication with beVault is handled via the `bevault-api-key` header passed from the MCP client. When configuring your MCP client, you need to:

1. **Create an API token** in beVault following the [beVault API Keys documentation](https://support.bevault.io/en/bevault-documentation/current-version/reference-guide/datafactory-user-reference-guide/datafactory-modules/client-admin/api-keys)

2. **Configure your MCP client** to include the following header in all requests:
   ```
   bevault-api-key: [your-api-token]
   ```
   Replace `[your-api-token]` with the actual API token you created.

3. The MCP server will forward this token to beVault's API for authentication.

**Important**: The permissions and project access assigned to your API token determine what operations the MCP server can perform. Make sure to configure the API key with appropriate rights for the projects and modules you need to access.

## Run

```bash
python -m bevault_mcp.main
```

The server will start an HTTP MCP server accessible at `http://localhost:8000/mcp`.

## Using with n8n

For a complete guide on integrating the beVault MCP server with n8n—including installation, API key setup, workflow configuration, and system prompts—see the [How to use beVault MCP Server with n8n](https://support.bevault.io/en/bevault-documentation/current-version/bevault-mcp-server/how-to-use-bevault-mcp-server-with-n8n) documentation.

## Development
- Code style and linting: ruff (see `CONTRIBUTING.md` for details)
- Python >= 3.13
- Uses FastMCP for HTTP/Streamable transport support

## Contributing

Contributions to this project are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) guide for details on development setup, code style, pre-commit hooks, and how to submit changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
