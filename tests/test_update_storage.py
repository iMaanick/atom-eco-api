import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_update_storage(client: TestClient, mock_storage_gateway, mock_uow):
    mock_storage_gateway.update_storage_by_id.return_value = 1
    storage_data = {
        "name": "Updated Storage",
        "location_x": 0,
        "location_y": 0,
        "capacities": [],
        "current_levels": []

    }

    response = client.put("/storages/1/", json=storage_data)
    assert response.status_code == 200
    assert response.json() == {"detail": "Storage updated successfully"}


@pytest.mark.asyncio
async def test_update_storage_not_found(client: TestClient, mock_storage_gateway, mock_uow):
    mock_storage_gateway.update_storage_by_id.return_value = None
    storage_data = {
        "name": "Updated Storage",
        "location_x": 0,
        "location_y": 0,
        "capacities": [],
        "current_levels": []
    }

    response = client.put("/storages/999/", json=storage_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Storage not found"}


@pytest.mark.asyncio
async def test_update_storage_missing_fields(client: TestClient, mock_storage_gateway, mock_uow):
    invalid_storage_data = {"name": "Updated Storage"}

    response = client.put("/storages/1/", json=invalid_storage_data)
    assert response.status_code == 422
