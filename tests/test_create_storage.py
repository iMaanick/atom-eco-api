import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_create_storage(client: TestClient, mock_storage_gateway, mock_uow):
    mock_storage_gateway.create_storage.return_value = 1
    storage_data = {
        "name": "Storage 1",
        "location_x": 0,
        "location_y": 0,
        "capacities": [],
        "current_levels": []
    }

    response = client.post("/storages/", json=storage_data)
    assert response.status_code == 200
    assert response.json() == {"storage_id": 1}


@pytest.mark.asyncio
async def test_create_storage_missing_fields(client: TestClient, mock_storage_gateway, mock_uow):
    invalid_storage_data = {"name": "Storage 1"}

    response = client.post("/storages/", json=invalid_storage_data)
    assert response.status_code == 422
