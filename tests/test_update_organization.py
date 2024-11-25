from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_update_organization(client: TestClient, mock_organization_gateway: AsyncMock) -> None:
    mock_organization_gateway.update_organization_by_id.return_value = 1

    organization_data = {
        "name": "Updated Org",
        "location_x": 0,
        "location_y": 0,
        "generated_waste": []
    }

    response = client.put("/organizations/1/", json=organization_data)

    assert response.status_code == 200
    assert response.json()["detail"] == "Organization updated successfully"


@pytest.mark.asyncio
async def test_update_organization_not_found(client: TestClient, mock_organization_gateway: AsyncMock) -> None:
    mock_organization_gateway.update_organization_by_id.return_value = None

    organization_data = {
        "name": "Updated Org",
        "location_x": 0,
        "location_y": 0,
        "generated_waste": []
    }

    response = client.put("/organizations/999/", json=organization_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found"
