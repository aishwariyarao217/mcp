"""
Copyright (c) 2026, Oracle and/or its affiliates.
Licensed under the Universal Permissive License v1.0 as shown at
https://oss.oracle.com/licenses/upl.
"""

from typing import Any

from pydantic import BaseModel, Field


class IntegrationSummary(BaseModel):
    id: str | None = Field(None, description="Integration composite identifier.")
    code: str | None = Field(None, description="Integration code.")
    version: str | None = Field(None, description="Integration version.")
    name: str | None = Field(None, description="Integration display name.")
    status: str | None = Field(None, description="Integration lifecycle status.")
    style: str | None = Field(None, description="Integration style, when present.")
    last_updated: str | None = Field(None, description="Last update timestamp.")


class IntegrationDetail(IntegrationSummary):
    description: str | None = Field(None, description="Integration description.")
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Original response payload for fields not yet normalized.",
    )


class ConnectionSummary(BaseModel):
    id: str | None = Field(None, description="Connection identifier.")
    name: str | None = Field(None, description="Connection display name.")
    identifier: str | None = Field(None, description="Connection adapter identifier.")
    role: str | None = Field(None, description="Connection role.")
    adapter_type: str | None = Field(None, description="Adapter type.")
    last_updated: str | None = Field(None, description="Last update timestamp.")


class ConnectionDetail(ConnectionSummary):
    description: str | None = Field(None, description="Connection description.")
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Original response payload for fields not yet normalized.",
    )


class ListResponse(BaseModel):
    count: int = Field(..., description="Number of returned items.")
    total_results: int | None = Field(None, description="Server-reported total result count.")
    has_more: bool | None = Field(None, description="Whether more results may be available.")
    offset: int | None = Field(None, description="Current page offset.")
    limit: int | None = Field(None, description="Current page limit.")
    items: list[dict[str, Any]] = Field(default_factory=list, description="Returned items.")


def _normalize_value(payload: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        if key in payload and payload[key] not in (None, ""):
            return payload[key]
    return None


def map_integration_summary(payload: dict[str, Any]) -> IntegrationSummary:
    return IntegrationSummary(
        id=_normalize_value(payload, "id"),
        code=_normalize_value(payload, "code"),
        version=_normalize_value(payload, "version"),
        name=_normalize_value(payload, "name"),
        status=_normalize_value(payload, "status"),
        style=_normalize_value(payload, "style"),
        last_updated=_normalize_value(payload, "lastUpdated", "last-updated"),
    )


def map_integration_detail(payload: dict[str, Any]) -> IntegrationDetail:
    summary = map_integration_summary(payload)
    return IntegrationDetail(
        **summary.model_dump(),
        description=_normalize_value(payload, "description"),
        payload=payload,
    )


def map_connection_summary(payload: dict[str, Any]) -> ConnectionSummary:
    return ConnectionSummary(
        id=_normalize_value(payload, "id"),
        name=_normalize_value(payload, "name"),
        identifier=_normalize_value(payload, "identifier"),
        role=_normalize_value(payload, "role"),
        adapter_type=_normalize_value(payload, "adapterType", "adapter-type"),
        last_updated=_normalize_value(payload, "lastUpdated", "last-updated"),
    )


def map_connection_detail(payload: dict[str, Any]) -> ConnectionDetail:
    summary = map_connection_summary(payload)
    return ConnectionDetail(
        **summary.model_dump(),
        description=_normalize_value(payload, "description"),
        payload=payload,
    )


def map_list_response(items: list[dict[str, Any]], payload: dict[str, Any]) -> ListResponse:
    return ListResponse(
        count=len(items),
        total_results=payload.get("totalResults") or payload.get("total-results"),
        has_more=payload.get("hasMore") or payload.get("has-more"),
        offset=payload.get("offset"),
        limit=payload.get("limit"),
        items=items,
    )
