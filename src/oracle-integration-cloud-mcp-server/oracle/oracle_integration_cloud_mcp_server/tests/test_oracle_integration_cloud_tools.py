"""
Copyright (c) 2026, Oracle and/or its affiliates.
Licensed under the Universal Permissive License v1.0 as shown at
https://oss.oracle.com/licenses/upl.
"""

from unittest.mock import Mock, patch

import pytest
from fastmcp import Client

from oracle.oracle_integration_cloud_mcp_server.server import mcp


class TestOracleIntegrationCloudTools:
    @pytest.mark.asyncio
    @patch("oracle.oracle_integration_cloud_mcp_server.server.get_oic_client")
    async def test_list_integrations(self, mock_get_client):
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.list_integrations.return_value = {
            "items": [
                {
                    "id": "SC2RN|01.00.0000",
                    "code": "SC2RN",
                    "version": "01.00.0000",
                    "name": "Sample Integration",
                    "status": "CONFIGURED",
                    "lastUpdated": "2026-03-18T18:00:00Z",
                }
            ],
            "offset": 0,
            "limit": 50,
            "hasMore": False,
            "totalResults": 1,
        }

        async with Client(mcp) as client:
            result = (await client.call_tool("list_integrations", {})).structured_content["result"]

        assert result["count"] == 1
        assert result["items"][0]["id"] == "SC2RN|01.00.0000"
        assert result["items"][0]["name"] == "Sample Integration"

    @pytest.mark.asyncio
    @patch("oracle.oracle_integration_cloud_mcp_server.server.get_oic_client")
    async def test_get_integration(self, mock_get_client):
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_integration.return_value = {
            "id": "SC2RN|01.00.0000",
            "code": "SC2RN",
            "version": "01.00.0000",
            "name": "Sample Integration",
            "description": "Read-only scaffold",
            "status": "CONFIGURED",
        }

        async with Client(mcp) as client:
            result = (
                await client.call_tool("get_integration", {"integration_id": "SC2RN|01.00.0000"})
            ).structured_content

        assert result["id"] == "SC2RN|01.00.0000"
        assert result["description"] == "Read-only scaffold"
        assert result["payload"]["status"] == "CONFIGURED"

    @pytest.mark.asyncio
    @patch("oracle.oracle_integration_cloud_mcp_server.server.get_oic_client")
    async def test_list_connections(self, mock_get_client):
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.list_connections.return_value = {
            "items": [
                {
                    "id": "rest_conn",
                    "name": "REST Connection",
                    "identifier": "REST",
                    "adapterType": "REST",
                    "role": "SOURCE_AND_TARGET",
                    "lastUpdated": "2026-03-18T18:00:00Z",
                }
            ],
            "offset": 0,
            "limit": 50,
            "hasMore": False,
            "totalResults": 1,
        }

        async with Client(mcp) as client:
            result = (await client.call_tool("list_connections", {})).structured_content["result"]

        assert result["count"] == 1
        assert result["items"][0]["id"] == "rest_conn"
        assert result["items"][0]["adapter_type"] == "REST"

    @pytest.mark.asyncio
    @patch("oracle.oracle_integration_cloud_mcp_server.server.get_oic_client")
    async def test_get_connection(self, mock_get_client):
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_connection.return_value = {
            "id": "rest_conn",
            "name": "REST Connection",
            "description": "Connection detail scaffold",
            "identifier": "REST",
            "adapterType": "REST",
            "role": "SOURCE_AND_TARGET",
        }

        async with Client(mcp) as client:
            result = (
                await client.call_tool("get_connection", {"connection_id": "rest_conn"})
            ).structured_content

        assert result["id"] == "rest_conn"
        assert result["description"] == "Connection detail scaffold"
        assert result["payload"]["identifier"] == "REST"

    @pytest.mark.asyncio
    @patch("oracle.oracle_integration_cloud_mcp_server.server.get_oic_client")
    async def test_list_integration_runs(self, mock_get_client):
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.list_integration_runs.return_value = {
            "items": [
                {
                    "id": "500400209",
                    "run-id": "42",
                    "status": "FAILED",
                    "integration-id": "SC2RN",
                    "integration-name": "Sample Integration",
                    "integration-version": "01.00.0000",
                    "creation-date": "2026-03-18T18:00:00Z",
                    "last-tracked-time": "2026-03-18T18:05:00Z",
                }
            ],
            "limit": 50,
            "has-more": False,
            "timeWindow": "24",
            "dataFetchTime": "2026-03-19T01:47:04.080+0000",
            "total-results": 1,
        }

        async with Client(mcp) as client:
            result = (await client.call_tool("list_integration_runs", {})).structured_content["result"]

        assert result["count"] == 1
        assert result["items"][0]["id"] == "500400209"
        assert result["items"][0]["run_id"] == "42"
        assert result["items"][0]["status"] == "FAILED"
        assert result["time_window"] == "24"
        assert result["data_fetch_time"] == "2026-03-19T01:47:04.080+0000"

    @pytest.mark.asyncio
    @patch("oracle.oracle_integration_cloud_mcp_server.server.get_oic_client")
    async def test_get_integration_run(self, mock_get_client):
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_integration_run.return_value = {
            "id": "500400209",
            "runId": "42",
            "status": "FAILED",
            "integrationName": "Sample Integration",
            "integrationVersion": "01.00.0000",
            "requestId": "req-123",
            "activityStream": ["Start", "Failure"],
        }

        async with Client(mcp) as client:
            result = (
                await client.call_tool("get_integration_run", {"run_id": "500400209"})
            ).structured_content

        assert result["id"] == "500400209"
        assert result["run_id"] == "42"
        assert result["payload"]["requestId"] == "req-123"

    @pytest.mark.asyncio
    @patch("oracle.oracle_integration_cloud_mcp_server.server.get_oic_client")
    async def test_list_failed_integration_runs(self, mock_get_client):
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.list_failed_integration_runs.return_value = {
            "items": [
                {
                    "id": "err-1",
                    "instanceId": "500400209",
                    "runId": "42",
                    "status": "FAILED",
                    "errorMessage": "Invoke failed",
                    "errorDetails": "Downstream returned 500",
                    "recoverable": True,
                    "retryCount": 1,
                    "integration": {
                        "code": "SC2RN",
                        "name": "Sample Integration",
                        "version": "01.00.0000",
                    },
                }
            ],
            "dataFetchTime": "2026-03-19T01:47:04.080+0000",
            "timeWindow": "1",
            "totalRecordsCount": 1,
            "has-more": False,
            "total-results": 1,
        }

        async with Client(mcp) as client:
            result = (
                await client.call_tool("list_failed_integration_runs", {})
            ).structured_content["result"]

        assert result["count"] == 1
        assert result["items"][0]["instance_id"] == "500400209"
        assert result["items"][0]["error_message"] == "Invoke failed"
        assert result["items"][0]["recoverable"] is True
        assert result["time_window"] == "1"
        assert result["data_fetch_time"] == "2026-03-19T01:47:04.080+0000"
        assert result["total_records_count"] == 1
