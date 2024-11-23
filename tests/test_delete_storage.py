import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_delete_storage(client: TestClient, mock_storage_gateway, mock_uow):
    mock_storage_gateway.delete_storage_by_id.return_value = 1

    response = client.delete("/storages/1/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Storage deleted successfully"}


@pytest.mark.asyncio
async def test_delete_storage_not_found(client: TestClient, mock_storage_gateway, mock_uow):
    mock_storage_gateway.delete_storage_by_id.return_value = None

    response = client.delete("/storages/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Storage not found"}
