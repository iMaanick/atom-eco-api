import pytest

from app.application.models import Organization, OrganizationWaste, WasteType
from app.application.models.storage import Storage


@pytest.mark.asyncio
async def test_get_distance_to_storage(client, mock_organization_gateway, mock_storage_gateway):
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[
            OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=1)
        ]
    )
    mock_storage_gateway.get_storage_by_id.return_value = Storage(
        id=2,
        name="S2",
        location_x=100,
        location_y=0,
        capacities=[],
        current_levels=[]
    )

    response = client.get("/organizations/1/distance-to-storage/2/")

    assert response.status_code == 200
    assert response.json()["distance"] == 100


@pytest.mark.asyncio
async def test_get_distance_to_storage_organization_not_found(client, mock_organization_gateway):
    mock_organization_gateway.get_organization_by_id.return_value = None

    response = client.get("/organizations/999/distance-to-storage/2/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid organization or storage"


@pytest.mark.asyncio
async def test_get_distance_to_storage_storage_not_found(client, mock_storage_gateway):
    mock_storage_gateway.get_storage_by_id.return_value = None

    response = client.get("/organizations/999/distance-to-storage/2/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid organization or storage"
