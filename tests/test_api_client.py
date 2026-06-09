import asyncio

import httpx
import pytest

from bot.api_client import ApiClient, ApiError
from log import log


def test_api_client_retries_on_transient_http_errors():
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(503, json={"detail": "Service unavailable"})
        return httpx.Response(200, json={"uuid": "abc123", "owner_token": "tok"})

    transport = httpx.MockTransport(handler)
    client = ApiClient("http://example.com", transport=transport)

    result = asyncio.run(client.create_box())

    assert result["uuid"] == "abc123"
    assert result["owner_token"] == "tok"
    assert len(calls) == 2


def test_api_client_maps_connect_error_to_api_error():
    async def handler(request: httpx.Request) -> httpx.Response:
        log.error("Connection failed")
        raise httpx.RequestError("Connection failed", request=request)

    transport = httpx.MockTransport(handler)
    client = ApiClient("http://example.com", transport=transport)

    with pytest.raises(ApiError) as excinfo:
        asyncio.run(client.create_box())

    assert excinfo.value.status_code == 503
    assert "unavailable" in excinfo.value.detail.lower()


def test_api_client_retries_until_timeout_error():
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        log.error("Gateway timeout")
        return httpx.Response(504, json={"detail": "Gateway timeout"})

    transport = httpx.MockTransport(handler)
    client = ApiClient("http://example.com", transport=transport)

    with pytest.raises(ApiError) as excinfo:
        asyncio.run(client.create_box())

    assert excinfo.value.status_code == 504
    assert len(calls) == client._max_retries + 1
