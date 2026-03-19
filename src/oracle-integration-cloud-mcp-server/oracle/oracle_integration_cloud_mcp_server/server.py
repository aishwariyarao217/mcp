"""
Copyright (c) 2026, Oracle and/or its affiliates.
Licensed under the Universal Permissive License v1.0 as shown at
https://oss.oracle.com/licenses/upl.
"""

import os
from logging import Logger
from typing import Literal, Optional

from fastmcp import FastMCP
from pydantic import Field

from . import __project__
from .client import OICClient
from .models import (
    ConnectionDetail,
    FailedIntegrationRunDetail,
    IntegrationDetail,
    IntegrationRunDetail,
    ListResponse,
    map_connection_detail,
    map_connection_summary,
    map_failed_integration_run_detail,
    map_failed_integration_run_summary,
    map_integration_detail,
    map_integration_run_detail,
    map_integration_run_summary,
    map_integration_summary,
    map_list_response,
)

logger = Logger(__name__, level="INFO")

mcp = FastMCP(
    name=__project__,
    instructions="""
        This server provides read-only tools for Oracle Integration Cloud (OIC).
        Use it to discover and inspect integrations and connections through typed
        tools backed by OIC Developer APIs.
    """,
)

ListOrderBy = Literal["name", "time"]


def get_oic_client() -> OICClient:
    return OICClient()


@mcp.tool(
    description="List Oracle Integration Cloud integrations with optional filtering and pagination."
)
def list_integrations(
    limit: Optional[int] = Field(None, description="Maximum number of items to return.", ge=1),
    offset: Optional[int] = Field(None, description="Starting offset for pagination.", ge=0),
    order_by: Optional[ListOrderBy] = Field(
        None,
        description="Sort order. Use 'name' or 'time'.",
    ),
    q: Optional[str] = Field(
        None,
        description="Optional OIC query filter string.",
    ),
    expand: Optional[str] = Field(
        None,
        description="Optional expand value such as 'connection' or 'connection.adapter'.",
    ),
) -> ListResponse:
    client = get_oic_client()
    payload = client.list_integrations(
        limit=limit,
        offset=offset,
        order_by=order_by,
        q=q,
        expand=expand,
    )
    items = [map_integration_summary(item).model_dump() for item in payload.get("items", [])]
    return map_list_response(items, payload)


@mcp.tool(description="Retrieve a single Oracle Integration Cloud integration by composite ID.")
def get_integration(
    integration_id: str = Field(
        ...,
        description="Composite integration ID, typically code|version.",
    ),
    expand: Optional[str] = Field(
        None,
        description="Optional expand value such as 'connection' or 'connection.adapter'.",
    ),
) -> IntegrationDetail:
    client = get_oic_client()
    payload = client.get_integration(integration_id, expand=expand)
    return map_integration_detail(payload)


@mcp.tool(
    description="List Oracle Integration Cloud connections with optional filtering and pagination."
)
def list_connections(
    limit: Optional[int] = Field(None, description="Maximum number of items to return.", ge=1),
    offset: Optional[int] = Field(None, description="Starting offset for pagination.", ge=0),
    order_by: Optional[str] = Field(
        None,
        description="Sort order, for example name, time, or adapter type depending on the API.",
    ),
    q: Optional[str] = Field(
        None,
        description="Optional OIC query filter string.",
    ),
    expand: Optional[str] = Field(
        None,
        description="Optional expand value. Valid value for OIC is typically 'adapter'.",
    ),
) -> ListResponse:
    client = get_oic_client()
    payload = client.list_connections(
        limit=limit,
        offset=offset,
        order_by=order_by,
        q=q,
        expand=expand,
    )
    items = [map_connection_summary(item).model_dump() for item in payload.get("items", [])]
    return map_list_response(items, payload)


@mcp.tool(description="Retrieve a single Oracle Integration Cloud connection by ID.")
def get_connection(
    connection_id: str = Field(..., description="Connection identifier."),
    expand: Optional[str] = Field(
        None,
        description="Optional expand value. Valid value for OIC is typically 'adapter'.",
    ),
) -> ConnectionDetail:
    client = get_oic_client()
    payload = client.get_connection(connection_id, expand=expand)
    return map_connection_detail(payload)


@mcp.tool(
    description="List Oracle Integration Cloud monitoring instances with optional filters and pagination."
)
def list_integration_runs(
    limit: Optional[int] = Field(None, description="Maximum number of items to return.", ge=1),
    offset: Optional[int] = Field(None, description="Starting offset for pagination.", ge=0),
    time_window: Optional[str] = Field(
        None,
        description="Optional OIC monitoring time window such as 1, 24, or 168, depending on the API semantics for your tenant.",
    ),
    q: Optional[str] = Field(
        None,
        description="Optional OIC monitoring filter, for example {code:'MYFLOW', timewindow:'1d'} or {status:'FAILED'}.",
    ),
    fields: Optional[str] = Field(
        None,
        description="Optional field limiter. Valid values include runId, id, and all.",
    ),
    group_by: Optional[str] = Field(
        None,
        description="Optional grouping. Valid value is typically integration.",
    ),
    return_mode: Optional[str] = Field(
        None,
        description="Optional return mode such as metadataminimal, metadata, minimal, or summary.",
    ),
) -> ListResponse:
    client = get_oic_client()
    payload = client.list_integration_runs(
        limit=limit,
        offset=offset,
        time_window=time_window,
        q=q,
        fields=fields,
        group_by=group_by,
        return_mode=return_mode,
    )
    items = [map_integration_run_summary(item).model_dump() for item in payload.get("items", [])]
    return map_list_response(items, payload)


@mcp.tool(description="Retrieve a single Oracle Integration Cloud monitoring instance by run ID.")
def get_integration_run(
    run_id: str = Field(..., description="Integration instance identifier."),
    return_mode: Optional[str] = Field(
        None,
        description="Optional return mode. Valid value includes minimal.",
    ),
) -> IntegrationRunDetail:
    client = get_oic_client()
    payload = client.get_integration_run(run_id, return_mode=return_mode)
    return map_integration_run_detail(payload)


@mcp.tool(
    description="List failed Oracle Integration Cloud runs using the errored instances monitoring endpoint."
)
def list_failed_integration_runs(
    limit: Optional[int] = Field(None, description="Maximum number of items to return.", ge=1),
    offset: Optional[int] = Field(None, description="Starting offset for pagination.", ge=0),
    time_window: Optional[str] = Field(
        None,
        description="Optional OIC monitoring time window such as 1, 24, or 168, depending on the API semantics for your tenant.",
    ),
    q: Optional[str] = Field(
        None,
        description="Optional OIC error filter, for example {code:'MYFLOW', timewindow:'1d'} or {recoverable:'true'}.",
    ),
    expand: Optional[str] = Field(
        None,
        description="Optional expansion. Valid values include integration and connection.",
    ),
    group_by: Optional[str] = Field(
        None,
        description="Optional grouping. Valid values include messages, integration, and connection.",
    ),
    return_mode: Optional[str] = Field(
        None,
        description="Optional return mode. Valid value includes minimal.",
    ),
) -> ListResponse:
    client = get_oic_client()
    payload = client.list_failed_integration_runs(
        limit=limit,
        offset=offset,
        time_window=time_window,
        q=q,
        expand=expand,
        group_by=group_by,
        return_mode=return_mode,
    )
    items = [map_failed_integration_run_summary(item).model_dump() for item in payload.get("items", [])]
    return map_list_response(items, payload)


def main():
    host = os.getenv("ORACLE_MCP_HOST")
    port = os.getenv("ORACLE_MCP_PORT")

    if host and port:
        mcp.run(transport="http", host=host, port=int(port))
    else:
        mcp.run()


if __name__ == "__main__":
    main()
