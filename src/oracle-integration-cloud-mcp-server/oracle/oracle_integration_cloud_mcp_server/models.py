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
    total_records_count: int | None = Field(
        None,
        description="Server-reported record count when provided by OIC monitoring APIs.",
    )
    has_more: bool | None = Field(None, description="Whether more results may be available.")
    offset: int | None = Field(None, description="Current page offset.")
    limit: int | None = Field(None, description="Current page limit.")
    time_window: str | None = Field(
        None,
        description="Applied OIC monitoring time window when present.",
    )
    data_fetch_time: str | None = Field(
        None,
        description="Timestamp when OIC generated the monitoring response.",
    )
    items: list[dict[str, Any]] = Field(default_factory=list, description="Returned items.")


class IntegrationRunSummary(BaseModel):
    id: str | None = Field(None, description="Integration instance identifier.")
    run_id: str | None = Field(None, description="Run identifier for scheduled integrations.")
    status: str | None = Field(None, description="Integration instance status.")
    integration_id: str | None = Field(None, description="Integration identifier.")
    integration_name: str | None = Field(None, description="Integration name.")
    integration_version: str | None = Field(None, description="Integration version.")
    creation_date: str | None = Field(None, description="Instance creation time.")
    last_tracked_time: str | None = Field(None, description="Last tracked time.")
    request_id: str | None = Field(None, description="Request identifier when present.")
    parent_instance_id: str | None = Field(None, description="Parent integration instance identifier.")
    primary_name: str | None = Field(None, description="Primary tracking name.")
    primary_value: str | None = Field(None, description="Primary tracking value.")


class IntegrationRunDetail(IntegrationRunSummary):
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Original response payload for fields not yet normalized.",
    )


class FailedIntegrationRunSummary(BaseModel):
    id: str | None = Field(None, description="Errored record identifier.")
    instance_id: str | None = Field(None, description="Integration instance identifier.")
    run_id: str | None = Field(None, description="Run identifier for scheduled integrations.")
    status: str | None = Field(None, description="Integration instance status.")
    integration_code: str | None = Field(None, description="Integration code, when present.")
    integration_name: str | None = Field(None, description="Integration name, when present.")
    integration_version: str | None = Field(None, description="Integration version, when present.")
    fault_id: str | None = Field(None, description="Fault identifier.")
    error_code: str | None = Field(None, description="Error code.")
    error_message: str | None = Field(None, description="Short error message.")
    error_details: str | None = Field(None, description="Detailed error message.")
    recoverable: bool | None = Field(None, description="Whether the errored run is recoverable.")
    retry_count: int | None = Field(None, description="Retry count.")
    creation_date: str | None = Field(None, description="Instance creation time.")
    last_tracked_time: str | None = Field(None, description="Last tracked time.")


class FailedIntegrationRunDetail(FailedIntegrationRunSummary):
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Original response payload for fields not yet normalized.",
    )


def _normalize_value(payload: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        if key in payload and payload[key] not in (None, ""):
            return payload[key]
    return None


def _normalize_bool(payload: dict[str, Any], *keys: str) -> bool | None:
    for key in keys:
        if key in payload and isinstance(payload[key], bool):
            return payload[key]
    return None


def _normalize_int(payload: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        if key in payload and isinstance(payload[key], int):
            return payload[key]
    return None


def _normalize_adapter_type(payload: dict[str, Any]) -> str | None:
    value = payload.get("adapterType")
    if isinstance(value, str) and value:
        return value
    if isinstance(value, dict):
        for key in ("displayName", "type", "name", "id"):
            nested = value.get(key)
            if isinstance(nested, str) and nested:
                return nested
    fallback = payload.get("adapter-type")
    if isinstance(fallback, str) and fallback:
        return fallback
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
        adapter_type=_normalize_adapter_type(payload),
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
        total_records_count=payload.get("totalRecordsCount") or payload.get("total-records-count"),
        has_more=payload.get("hasMore") if "hasMore" in payload else payload.get("has-more"),
        offset=payload.get("offset"),
        limit=payload.get("limit"),
        time_window=payload.get("timeWindow") or payload.get("time-window"),
        data_fetch_time=payload.get("dataFetchTime") or payload.get("data-fetch-time"),
        items=items,
    )


def map_integration_run_summary(payload: dict[str, Any]) -> IntegrationRunSummary:
    return IntegrationRunSummary(
        id=_normalize_value(payload, "id", "instance-id"),
        run_id=_normalize_value(payload, "runId", "run-id"),
        status=_normalize_value(payload, "status"),
        integration_id=_normalize_value(payload, "integrationId", "integration-id"),
        integration_name=_normalize_value(payload, "integrationName", "integration-name"),
        integration_version=_normalize_value(payload, "integrationVersion", "integration-version"),
        creation_date=_normalize_value(payload, "creationDate", "creation-date"),
        last_tracked_time=_normalize_value(payload, "lastTrackedTime", "last-tracked-time"),
        request_id=_normalize_value(payload, "requestId", "request-id"),
        parent_instance_id=_normalize_value(payload, "parentInstanceId", "parent-instance-id"),
        primary_name=_normalize_value(payload, "primaryName", "pk-name"),
        primary_value=_normalize_value(payload, "primaryValue", "pk-value"),
    )


def map_integration_run_detail(payload: dict[str, Any]) -> IntegrationRunDetail:
    summary = map_integration_run_summary(payload)
    return IntegrationRunDetail(
        **summary.model_dump(),
        payload=payload,
    )


def map_failed_integration_run_summary(payload: dict[str, Any]) -> FailedIntegrationRunSummary:
    integration = payload.get("integration") if isinstance(payload.get("integration"), dict) else {}
    return FailedIntegrationRunSummary(
        id=_normalize_value(payload, "id"),
        instance_id=_normalize_value(payload, "instanceId", "instance-id"),
        run_id=_normalize_value(payload, "runId", "run-id"),
        status=_normalize_value(payload, "status"),
        integration_code=_normalize_value(payload, "code", "integrationId", "integration-id")
        or _normalize_value(integration, "code", "id"),
        integration_name=_normalize_value(payload, "integrationName", "integration-name")
        or _normalize_value(integration, "name", "displayName"),
        integration_version=_normalize_value(payload, "integrationVersion", "integration-version")
        or _normalize_value(integration, "version"),
        fault_id=_normalize_value(payload, "faultId", "fault-id"),
        error_code=_normalize_value(payload, "errorCode", "error-code"),
        error_message=_normalize_value(payload, "errorMessage", "error-message"),
        error_details=_normalize_value(payload, "errorDetails", "error-details"),
        recoverable=_normalize_bool(payload, "recoverable"),
        retry_count=_normalize_int(payload, "retryCount", "retry-count"),
        creation_date=_normalize_value(payload, "creationDate", "creation-date"),
        last_tracked_time=_normalize_value(payload, "lastTrackedTime", "last-tracked-time"),
    )


def map_failed_integration_run_detail(payload: dict[str, Any]) -> FailedIntegrationRunDetail:
    summary = map_failed_integration_run_summary(payload)
    return FailedIntegrationRunDetail(
        **summary.model_dump(),
        payload=payload,
    )
