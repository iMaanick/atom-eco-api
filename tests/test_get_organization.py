from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient

from app.application.models import OrganizationWaste, Organization, WasteType


@pytest.mark.asyncio
async def test_get_organization(client: TestClient, mock_organization_gateway: AsyncMock) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[
            OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=1)
        ]
    )
    response = client.get("/organizations/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Org 1"


@pytest.mark.asyncio
async def test_get_organization_not_found(client: TestClient, mock_organization_gateway: AsyncMock) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = None

    response = client.get("/organizations/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Data not found for specified organization_id."
