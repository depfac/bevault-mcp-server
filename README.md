# bevault-mcp

## Introduction

This is the MCP (Model Context Protocol) server for [beVault](https://www.bevault.io/), a modern data platform designed to manage scalable, secure, and auditable data using Data Vault methodology.

This MCP server allows you to perform actions that users can do in the following beVault modules:
- **Build**: Create and manage data models (Hubs, Links, Satellites, Reference Tables)
- **Source**: Manage source systems, data packages, and staging tables
- **Distribute**: Create and manage information marts and their scripts

> **Note**: Support for the **Verify** module will be added in a future release.

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

Or use docker-compose with environment variables configured in your compose file.

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

### Authentication

Authentication with beVault is handled via the `Authorization` header passed from the MCP client. When configuring your MCP client, you need to:

1. **Create an API token** in beVault following the [beVault API Keys documentation](https://support.bevault.io/en/bevault-documentation/current-version/reference-guide/datafactory-user-reference-guide/datafactory-modules/client-admin/api-keys)

2. **Configure your MCP client** to include the following header in all requests:
   ```
   Authorization: ApiToken [your-api-token]
   ```
   Replace `[your-api-token]` with the actual API token you created.

3. The MCP server will forward this `Authorization` header to beVault's API for authentication.

**Important**: The permissions and project access assigned to your API token determine what operations the MCP server can perform. Make sure to configure the API key with appropriate rights for the projects and modules you need to access.

## Run

```bash
python -m bevault_mcp.main
```

The server will start an HTTP MCP server accessible at `http://localhost:8000/mcp`.

## Using with n8n

### 1. Expose the Server (if needed)

If your n8n instance is running in a different environment (e.g., Docker), you may need to expose the MCP server:

- **Local n8n**: Use `http://localhost:8000/mcp` or `http://host.docker.internal:8000/mcp` if n8n is in Docker
- **Remote n8n**: Use ngrok or similar service to expose your local server:
  ```bash
  ngrok http 8000
  ```
  This will provide a public URL like `https://abc123.ngrok.io`

### 2. Configure n8n MCP Client Tool

In n8n, create an AI agent using any LLM model and add an MCP Client Tool node with the following configuration:

**Node Parameters:**
- **Endpoint URL**: The URL of your MCP server (e.g., `http://host.docker.internal:8000/mcp` or `https://abc123.ngrok.io/mcp`)
- **Authentication**: Select "Header Auth"
- **Options**: Leave as default (empty object)

**Credentials Setup:**

Create credentials in n8n for the MCP Client Tool:

1. **Credential Type**: Header Auth
2. **Name**: `Authorization` (this is the header name)
3. **Value**: `ApiToken [your-api-token]` where `[your-api-token]` is the API token you created in beVault

**Example**: If your API token is `sk_abc123xyz789`, the value should be:
```
ApiToken sk_abc123xyz789
```

**Important**: The API token must be prefixed with `ApiToken ` (with a space) as required by beVault's API authentication format.



## Development
- Code style and linting: ruff (see `CONTRIBUTING.md` for details)
- Python >= 3.13
- Uses FastMCP for HTTP/Streamable transport support

## Contributing

Contributions to this project are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) guide for details on development setup, code style, pre-commit hooks, and how to submit changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
