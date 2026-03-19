"""
Copyright (c) 2026, Oracle and/or its affiliates.
Licensed under the Universal Permissive License v1.0 as shown at
https://oss.oracle.com/licenses/upl.
"""

import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import requests

from . import __project__, __version__


class OICConfigurationError(ValueError):
    """Raised when required OIC configuration is missing."""


@dataclass(slots=True)
class OICSettings:
    base_url: str
    integration_instance: str
    token_url: str
    client_id: str
    client_secret: str
    scope: str | None
    verify_ssl: bool
    timeout_seconds: float
    user_agent: str

    @classmethod
    def from_env(cls) -> "OICSettings":
        required = {
            "OIC_BASE_URL": os.getenv("OIC_BASE_URL"),
            "OIC_INTEGRATION_INSTANCE": os.getenv("OIC_INTEGRATION_INSTANCE"),
            "OIC_TOKEN_URL": os.getenv("OIC_TOKEN_URL"),
            "OIC_CLIENT_ID": os.getenv("OIC_CLIENT_ID"),
            "OIC_CLIENT_SECRET": os.getenv("OIC_CLIENT_SECRET"),
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise OICConfigurationError(
                "Missing required OIC configuration: " + ", ".join(sorted(missing))
            )

        verify_ssl_raw = (os.getenv("OIC_VERIFY_SSL") or "true").strip().lower()
        verify_ssl = verify_ssl_raw not in {"0", "false", "no"}
        timeout_seconds = float(os.getenv("OIC_HTTP_TIMEOUT_SECONDS", "30"))

        return cls(
            base_url=required["OIC_BASE_URL"].rstrip("/"),
            integration_instance=required["OIC_INTEGRATION_INSTANCE"],
            token_url=required["OIC_TOKEN_URL"],
            client_id=required["OIC_CLIENT_ID"],
            client_secret=required["OIC_CLIENT_SECRET"],
            scope=os.getenv("OIC_SCOPE"),
            verify_ssl=verify_ssl,
            timeout_seconds=timeout_seconds,
            user_agent=f"{__project__}/{__version__}",
        )


class OICClient:
    """Small REST client for a read-only subset of OIC Developer APIs."""

    def __init__(self, settings: OICSettings | None = None, session: requests.Session | None = None):
        self.settings = settings or OICSettings.from_env()
        self.session = session or requests.Session()
        self._access_token: str | None = None
        self._expires_at: float = 0.0

    def _get_access_token(self) -> str:
        now = time.time()
        if self._access_token and now < self._expires_at:
            return self._access_token

        payload = {"grant_type": "client_credentials"}
        if self.settings.scope:
            payload["scope"] = self.settings.scope

        response = self.session.post(
            self.settings.token_url,
            data=payload,
            auth=(self.settings.client_id, self.settings.client_secret),
            headers={
                "Accept": "application/json",
                "User-Agent": self.settings.user_agent,
            },
            timeout=self.settings.timeout_seconds,
            verify=self.settings.verify_ssl,
        )
        response.raise_for_status()
        body = response.json()

        access_token = body.get("access_token")
        if not access_token:
            raise OICConfigurationError("Token response did not include access_token")

        expires_in = int(body.get("expires_in", 300))
        self._access_token = access_token
        self._expires_at = now + max(expires_in - 30, 30)
        return access_token

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        token = self._get_access_token()
        merged_params = {"integrationInstance": self.settings.integration_instance}
        if params:
            merged_params.update({key: value for key, value in params.items() if value is not None})

        response = self.session.request(
            method=method,
            url=f"{self.settings.base_url}{path}",
            params=merged_params,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "User-Agent": self.settings.user_agent,
            },
            timeout=self.settings.timeout_seconds,
            verify=self.settings.verify_ssl,
        )
        response.raise_for_status()
        return response.json()

    def list_integrations(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
        q: str | None = None,
        expand: str | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            "/ic/api/integration/v1/integrations",
            params={
                "limit": limit,
                "offset": offset,
                "orderBy": order_by,
                "q": q,
                "expand": expand,
            },
        )

    def get_integration(self, integration_id: str, *, expand: str | None = None) -> dict[str, Any]:
        encoded_id = quote(integration_id, safe="")
        return self._request(
            "GET",
            f"/ic/api/integration/v1/integrations/{encoded_id}",
            params={"expand": expand},
        )

    def list_connections(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
        q: str | None = None,
        expand: str | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            "/ic/api/integration/v1/connections",
            params={
                "limit": limit,
                "offset": offset,
                "orderBy": order_by,
                "q": q,
                "expand": expand,
            },
        )

    def get_connection(self, connection_id: str, *, expand: str | None = None) -> dict[str, Any]:
        encoded_id = quote(connection_id, safe="")
        return self._request(
            "GET",
            f"/ic/api/integration/v1/connections/{encoded_id}",
            params={"expand": expand},
        )

    def list_integration_runs(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        q: str | None = None,
        fields: str | None = None,
        group_by: str | None = None,
        return_mode: str | None = None,
        time_window: str | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            "/ic/api/integration/v1/monitoring/instances",
            params={
                "limit": limit,
                "offset": offset,
                "q": q,
                "fields": fields,
                "groupBy": group_by,
                "return": return_mode,
                "timeWindow": time_window,
            },
        )

    def get_integration_run(self, run_id: str, *, return_mode: str | None = None) -> dict[str, Any]:
        encoded_id = quote(run_id, safe="")
        return self._request(
            "GET",
            f"/ic/api/integration/v1/monitoring/instances/{encoded_id}",
            params={"return": return_mode},
        )

    def list_failed_integration_runs(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        q: str | None = None,
        expand: str | None = None,
        group_by: str | None = None,
        return_mode: str | None = None,
        time_window: str | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            "/ic/api/integration/v1/monitoring/errors",
            params={
                "limit": limit,
                "offset": offset,
                "q": q,
                "expand": expand,
                "groupBy": group_by,
                "return": return_mode,
                "timeWindow": time_window,
            },
        )
