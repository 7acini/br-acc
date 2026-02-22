import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_entity_lookup_rejects_invalid_format(client: AsyncClient) -> None:
    response = await client.get("/api/v1/entity/abc")
    assert response.status_code == 400
    assert "Invalid CPF or CNPJ" in response.json()["detail"]


@pytest.mark.anyio
async def test_entity_lookup_rejects_short_number(client: AsyncClient) -> None:
    response = await client.get("/api/v1/entity/12345")
    assert response.status_code == 400


@pytest.mark.anyio
async def test_entity_lookup_rejects_15_digits(client: AsyncClient) -> None:
    response = await client.get("/api/v1/entity/123456789012345")
    assert response.status_code == 400


@pytest.mark.anyio
async def test_connections_rejects_invalid_depth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/entity/test-id/connections?depth=5")
    assert response.status_code == 422


@pytest.mark.anyio
async def test_connections_rejects_zero_depth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/entity/test-id/connections?depth=0")
    assert response.status_code == 422
