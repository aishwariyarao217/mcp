# Oracle Integration Cloud MCP Server

## Overview

This server provides a FastMCP wrapper around a small, read-only subset of the
Oracle Integration Cloud (OIC) REST APIs.

The initial scaffold focuses on the most useful discovery and inspection flows:

- list integrations
- inspect a single integration
- list connections
- inspect a single connection

## Status

This directory is currently a scaffold for a new MCP server contribution. The
tool surface is intentionally small so we can iterate safely before adding
write-capable or operational workflows.

## Configuration

Set the following environment variables before starting the server:

- `OIC_BASE_URL`: Base Oracle Integration URL, for example `https://<host>`
- `OIC_INTEGRATION_INSTANCE`: Service instance name used by OIC Developer APIs
- `OIC_TOKEN_URL`: OAuth token endpoint
- `OIC_CLIENT_ID`: OAuth client ID
- `OIC_CLIENT_SECRET`: OAuth client secret

Optional environment variables:

- `OIC_SCOPE`: OAuth scope to request
- `OIC_VERIFY_SSL`: `true` or `false`, defaults to `true`
- `ORACLE_MCP_HOST`: Bind host for HTTP transport
- `ORACLE_MCP_PORT`: Bind port for HTTP transport

## Running the server

### STDIO transport mode

```sh
uvx oracle.oracle-integration-cloud-mcp-server
```

### HTTP streaming transport mode

```sh
ORACLE_MCP_HOST=127.0.0.1 ORACLE_MCP_PORT=8888 uvx oracle.oracle-integration-cloud-mcp-server
```

## Tools

| Tool Name | Description |
| --- | --- |
| `list_integrations` | List integrations with optional filters and pagination |
| `get_integration` | Retrieve a single integration by composite ID |
| `list_connections` | List connections with optional filters and pagination |
| `get_connection` | Retrieve a single connection by ID |

## Notes

- This scaffold currently targets read-only Developer API operations only.
- Authentication is handled with OAuth client credentials.
- The API client layer is isolated in `client.py` so we can extend auth and
  endpoint support without changing the MCP tool contracts.

## License

Copyright (c) 2026 Oracle and/or its affiliates.

Released under the Universal Permissive License v1.0 as shown at
<https://oss.oracle.com/licenses/upl/>.
