import pytest
from starlette.testclient import TestClient

from app.application.models.storage import Storage


@pytest.mark.asyncio
async def test_get_storages(client: TestClient, mock_storage_gateway):
    mock_storage_gateway.get_storages.return_value = [
        Storage(id=1, name="Storage 1", location_x=0, location_y=0, capacities=[], current_levels=[]),
        Storage(id=2, name="Storage 2", location_x=10, location_y=10, capacities=[], current_levels=[])
    ]
    response = client.get("/storages/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Storage 1"
    assert response.json()[1]["name"] == "Storage 2"


@pytest.mark.asyncio
async def test_get_storages_empty(client: TestClient, mock_storage_gateway):
    mock_storage_gateway.get_storages.return_value = []

    response = client.get("/storages/")
    assert response.status_code == 200
    assert len(response.json()) == 0
