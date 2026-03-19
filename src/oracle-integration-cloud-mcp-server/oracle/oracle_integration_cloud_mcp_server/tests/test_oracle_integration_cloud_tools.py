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
