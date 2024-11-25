from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient

from app.application.models.storage import Storage


@pytest.mark.asyncio
async def test_get_storage(client: TestClient, mock_storage_gateway: AsyncMock) -> None:
    mock_storage_gateway.get_storage_by_id.return_value = Storage(id=1, name="Storage 1", location_x=0, location_y=0,
                                                                  capacities=[], current_levels=[])

    response = client.get("/storages/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Storage 1"


@pytest.mark.asyncio
async def test_get_storage_not_found(client: TestClient, mock_storage_gateway: AsyncMock) -> None:
    mock_storage_gateway.get_storage_by_id.return_value = None

    response = client.get("/storages/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Storage not found"}
