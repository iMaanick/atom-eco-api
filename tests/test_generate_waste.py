from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_generate_waste(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_uow: AsyncMock
) -> None:
    mock_organization_gateway.generate_waste.return_value = None
    params = {
        "waste_type": "BIO_WASTE",
        "amount": 50
    }
    response = client.get(f"/organizations/1/generate_waste/", params=params)

    assert response.status_code == 200
    assert response.json() == {"detail": f"Successfully added 50 of BIO_WASTE waste to organization 1."}

    mock_organization_gateway.generate_waste.assert_called_once_with(1, "BIO_WASTE", 50)


@pytest.mark.asyncio
async def test_generate_waste_not_found(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_uow: AsyncMock
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = None
    params = {
        "waste_type": "BIO_WASTE",
        "amount": 60
    }
    response = client.get(f"/organizations/1/generate_waste/", params=params)

    assert response.status_code == 404
    assert response.json() == {"detail": f"Organization not found"}

