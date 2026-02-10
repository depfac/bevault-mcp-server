# bevault-mcp

Minimal MCP server for beVault that exposes tools to query beVault's API using FastMCP with HTTP transport.

## Features
- `search_model`: search entities (Hubs, Links, Satellites, ReferenceTables) in a beVault project
- `search_information_marts`: search and list information marts (with simplified script info)
- `get_information_mart_script`: retrieve full information mart script definition (metadata + columns + sources)
- `search_source_systems`: search source systems and their data packages (with staging table info)
- `create_*` / `update_*` / `delete_*` tools for hubs, links, source systems, data packages, information marts and scripts
- `create_staging_table` and column tools to define and evolve staging tables
- Mapping tools (`map_column_to_hub`, `map_columns_to_link`, `map_columns_to_satellite`, delete/update mapping helpers)
- Introspection tools like `get_link`, `get_satellite`, `get_staging_table`, `get_snapshots`

## Install

```bash
pip install -e .
```

Or, using the `pyproject.toml` metadata:

```bash
pip install -e ".[dev]"
```

## Configure

### 1. Environment Setup
Create a `.env` file in the project root:

```ini
BEVAULT_BASE_URL=https://bevault.metavault.url.com
REQUEST_TIMEOUT_SECONDS=30
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

- `BEVAULT_BASE_URL`: The base URL of your beVault instance (required)
- `REQUEST_TIMEOUT_SECONDS`: HTTP request timeout in seconds (default: 30)
- `MCP_HOST` and `MCP_PORT`: Server host and port (optional, defaults to `0.0.0.0:8000`)

### 2. API Token Setup

To use this MCP server, you need to create an API token in beVault. The actions allowed by the MCP server depend on the rights granted to the API token.

1. Start the MCP server (see Run section below)
2. Configure the beVault URL in your `.env` file
3. Follow the [beVault API Keys documentation](https://support.bevault.io/en/bevault-documentation/current-version/reference-guide/datafactory-user-reference-guide/datafactory-modules/client-admin/api-keys) to create an API token
4. The API token will be used by clients connecting to the MCP server via the `Authorization` header

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

## Tools

### Model search

#### `search_model`
Search entities in the beVault model (Hubs, Links, Satellites, ReferenceTables) and return an optimized, paginated result.

- **params**:
  - `searchString` (str, optional): Free-text search string
  - `projectName` (str, optional): Project name (if omitted, client default is used)
  - `index` (int, default 0): Page index
  - `limit` (int, default 10): Page size
  - `includeHubs` (bool, default true)
  - `includeLinks` (bool, default true)
  - `includeSatellites` (bool, default true)
  - `includeReferenceTables` (bool, default true)
- **returns**: optimized paging info and a list of hubs/links/satellites/reference tables with key fields

### Information marts

#### `search_information_marts`
Search information marts in a beVault project and return an optimized list with simplified script info.

- **params**:
  - `projectName` (str, required): Project name (resolved to project ID)
  - `searchName` (str, optional): Filter by mart name (`name contains searchName`)
  - `index` (int, default 0): Page index
  - `limit` (int, default 10): Page size
- **returns**: paging info and information marts with basic metadata and a simplified `scripts` list

#### `get_information_mart_script`
Get a full information mart script (metadata, columns, `sourceColumns`) by project, mart and script identifiers.

- **params**:
  - `projectName` (str, required)
  - `informationMartIdOrName` (str, required): Mart ID or name
  - `scriptIdOrName` (str, required): Script ID or name
- **returns**: full script entity as JSON

#### `create_information_mart` / `update_information_mart`
Create or update an information mart.

- **core params**:
  - `projectName` (str, required)
  - `informationMartIdOrName` (str, required for update)
  - `name` (str, required)
  - `schema` (str, required): Database schema name
  - `prefix` (str, optional): Table prefix
  - `snapshotIdOrName` (str, optional): Snapshot ID or name
  - `businessDescription` / `technicalDescription` (str, optional)

#### `create_information_mart_script`
Create a new script under an information mart (with optional order, timeout and table name).

#### `update_information_mart_script`
Update script metadata (name, order, timeout, table name, tags, descriptions, columns and their `sourceColumns`) while preserving code.

#### `update_information_mart_script_code`
Update only the SQL code of a script (metadata is preserved).

#### `get_snapshots`
List snapshots for a project (used to attach marts to snapshots).

#### `delete_information_mart` / `delete_information_mart_script`
Delete an information mart or a single mart script by project and mart/script identifiers.

### Hubs

#### `create_hub`
Create a hub in a beVault project.

### create_hub
Create a hub in a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `name` (str, required): Name of the hub (must be unique)
  - `ignoreBusinessKeyCase` (bool, default false): Whether to ignore case in business key
  - `businessKeyLength` (int, default 255): Length of the business key
  - `technicalDescription` (str, optional): Technical description of the hub
  - `businessDescription` (str, optional): Business description of the hub
- **returns**: The created hub entity as a dictionary

#### `update_hub`
Update a hub in a beVault project (same shape as `create_hub`, plus `hubIdOrName`).

#### `delete_hub`
Delete a hub by ID or name.

### Links

#### `create_link`
Create a link in a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `name` (str, required): Name of the link (must be unique)
  - `linkType` (str, default "Relationship"): Type of link - Relationship, Hierarchy, Transaction, or SameAs
  - `dependentChildColumns` (list[dict], optional): List of dependent child columns, each with `columnName` and `dataType`
  - `hubReferences` (list[dict], optional): List of hub references, each with `columnName`, `hubName`, and `order`. The `hubName` will be resolved to a hub URL
  - `technicalDescription` (str, optional): Technical description of the link
  - `businessDescription` (str, optional): Business description of the link
- **returns**: The created link entity as a dictionary

#### `get_link`
Get a link (including hub references, dependent children, data columns) by `linkIdOrName`.

#### `update_link`
Update a link (same shape as `create_link`, plus `linkIdOrName`).

#### `delete_link`
Delete a link by ID or name.

### Satellites

#### `get_satellite`
Get a satellite by project, parent type (`"hub"` or `"link"`), parent ID/name and satellite ID/name.

### Source systems and data packages

#### `create_source_system`
Create a source system in a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `name` (str, required): Name of the source system (must be unique)
  - `code` (str, required): Code of the source system
  - `version` (str, optional): Version of the source system
  - `qualityType` (int, optional): Quality type of the source system (integer between 1 and 4)
  - `technicalDescription` (str, optional): Technical description of the source system
  - `businessDescription` (str, optional): Business description of the source system
  - `dataSteward` (str, optional): Data steward responsible for the source system
  - `systemAdministrator` (str, optional): System administrator for the source system
- **returns**: The created source system entity as a dictionary (note: `qualityType` in the response is returned as a string like "Good", "Excellent", etc.)

#### `create_data_package`
Create a data package in a source system within a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `sourceSystemName` (str, required): Name or ID of the source system
  - `name` (str, required): Name of the data package (must be unique)
  - `deliverySchedule` (str, optional): Delivery schedule of the data package (e.g., "Daily")
  - `technicalDescription` (str, optional): Technical description of the data package
  - `businessDescription` (str, optional): Business description of the data package
  - `refreshType` (str, optional): Refresh type of the data package (e.g., "automatic")
  - `formatInfo` (str, optional): Format information of the data package
  - `expectedQuality` (int, optional): Expected quality of the data package (integer)
- **returns**: The created data package entity as a dictionary

#### `search_source_systems`
Search source systems and include their data packages plus basic staging table info.

- **params**:
  - `projectName` (str, required)
  - `contains` (str, optional): Filter `name contains contains`
  - `index` (int, default 0)
  - `limit` (int, default 10)
- **returns**: paging info and a list of source systems, each with `packages` and their `stagingTables`

#### `update_source_system`
Update a source system in a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `sourceSystemIdOrName` (str, required): ID (GUID) or name of the source system to update
  - `name` (str, required): Name of the source system (must be unique)
  - `code` (str, required): Code of the source system
  - `version` (str, optional): Version of the source system
  - `qualityType` (int, optional): Quality type of the source system (integer)
  - `technicalDescription` (str, optional): Technical description of the source system
  - `businessDescription` (str, optional): Business description of the source system
  - `dataSteward` (str, optional): Data steward responsible for the source system
  - `systemAdministrator` (str, optional): System administrator for the source system
- **returns**: The updated source system entity as a dictionary

#### `delete_source_system`
Delete a source system from a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `sourceSystemIdOrName` (str, required): ID (GUID) or name of the source system to delete
- **returns**: A confirmation message as a dictionary

#### `update_data_package`
Update a data package in a source system within a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `sourceSystemIdOrName` (str, required): ID (GUID) or name of the source system
  - `dataPackageIdOrName` (str, required): ID (GUID) or name of the data package to update
  - `name` (str, required): Name of the data package (must be unique)
  - `deliverySchedule` (str, optional): Delivery schedule of the data package (e.g., "Daily")
  - `technicalDescription` (str, optional): Technical description of the data package
  - `businessDescription` (str, optional): Business description of the data package
  - `refreshType` (str, optional): Refresh type of the data package (e.g., "automatic")
  - `formatInfo` (str, optional): Format information of the data package
  - `expectedQuality` (int, optional): Expected quality of the data package (integer)
- **returns**: The updated data package entity as a dictionary

#### `delete_data_package`
Delete a data package from a source system in a beVault project.

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `sourceSystemIdOrName` (str, required): ID (GUID) or name of the source system
  - `dataPackageIdOrName` (str, required): ID (GUID) or name of the data package to delete
- **returns**: A confirmation message as a dictionary

### Staging tables

#### `create_staging_table`
Create a staging table in a data package within a beVault project.

Staging tables can be created in 4 different ways:

1. **Column list**: Provide a structured list of columns with their definitions
2. **View**: Provide a SELECT statement to create a view
3. **DDL Table**: Provide DDL column definitions as text (column names and types)
4. **Existing table**: Reference an existing table in the stg schema (just provide tableName)

- **params**:
  - `projectName` (str, required): Name of the project (will be resolved to project ID)
  - `sourceSystemIdOrName` (str, required): ID (GUID) or name of the source system
  - `dataPackageIdOrName` (str, required): ID (GUID) or name of the data package
  - `tableName` (str, required): Name of the staging table (must be unique)
  - `queryType` (str, required): Type of table - "Table" or "View"
  - `query` (str, optional): 
    - For DDL Table: Column definitions as text (e.g., `"id text, name text, sign_date timestamp"`)
    - For View: SELECT statement (e.g., `"SELECT *, 'hardcoded' as hardcoded_value FROM stg.odoo19_contracts"`)
    - For Existing table: Omit or use empty string
    - For Column list: Omit or use empty string
  - `columns` (list[dict], optional): List of column definitions (only for column list creation). Each column dict contains:
    - `name` (str, required): Column name
    - `dataType` (str, required): Column type. User-friendly types (DateTime, Date, Text, Boolean, Integer, Numeric) are automatically mapped to API types (DateTime2, Date, String, Boolean, Int32, VarNumeric). You can also use API types directly.
    - `nullable` (bool, optional): Whether column is nullable (default: True)
    - `primaryKey` (bool, optional): Whether column is a primary key (default: False)
    - `length` (int, optional): Length for String/Text types (required for Text/String dataType)
    - `businessDescription` (str, optional): Business description of the column
    - `businessName` (str, optional): Business name of the column
    - `technicalDescription` (str, optional): Technical description of the column

- **returns**: The created staging table entity as a dictionary, including column definitions if created via column list

#### `add_staging_table_column`
Add a new column to an existing staging table (supporting user-friendly and API data types, base type, and hard rules).

#### `update_staging_table_column`
Update an existing staging table column (same shape as `add_staging_table_column`, plus `columnId`).

#### `get_staging_table`
Return a staging table with its columns and a user-friendly list of hub/link/satellite mappings to that table.

#### `delete_staging_table_column`
Delete a staging table column by ID.

### Mappings

#### `map_column_to_hub`
Map a single staging table column to a hub (creates a hub mapping used to generate Hubs + effectivity satellites).

#### `map_columns_to_link`
Map hub references, dependent child columns and data columns from a staging table to a link.  
You must create the hub mappings first and then map the link, providing all link components you want mapped.

#### `map_columns_to_satellite`
Create a satellite mapping by attaching selected staging columns to a hub or link mapping, optionally as multi-active.

#### `delete_staging_table_mapping`
Delete a hub, link or satellite mapping from a staging table (type and correct API path are resolved automatically).

#### `update_staging_table_satellite_mapping`
Update an existing satellite mapping (name, columns, multi-active flags and subsequence column).

## Development
- Code style: black + isort
- Python >= 3.9
- Uses FastMCP for HTTP/Streamable transport support
