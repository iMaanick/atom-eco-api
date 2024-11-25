from unittest.mock import AsyncMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient

from app.application.models import OrganizationWaste, WasteType, Organization
from app.application.models.storage import Storage
from app.application.models.storage_capacity import StorageCapacity
from app.application.models.storage_current_level import StorageCurrentLevel


@pytest.mark.asyncio
async def test_transfer_waste_to_specific_storage(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_transfer_waste = AsyncMock(return_value=None)
    monkeypatch.setattr("app.api.organizations.transfer_waste", mock_transfer_waste)

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
        capacities=[
            StorageCapacity(
                waste_type=WasteType.BIO_WASTE,
                capacity=2
            )
        ],
        current_levels=[
            StorageCurrentLevel(
                waste_type=WasteType.BIO_WASTE,
                current_amount=1
            )
        ]
    )

    transfer_request = {
        "waste_type": "BIO_WASTE",
        "amount": 1
    }

    response = client.post("/organizations/1/storages/2/transfer-waste/", json=transfer_request)
    assert response.status_code == 200
    assert response.json() == {"detail": "Waste transferred successfully."}
    mock_organization_gateway.get_organization_by_id.assert_called_once_with(1)
    mock_storage_gateway.get_storage_by_id.assert_called_once_with(2)


@pytest.mark.asyncio
async def test_organization_not_found(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = None
    transfer_request = {
        "waste_type": "BIO_WASTE",
        "amount": 1
    }
    response = client.post("/organizations/1/storages/1/transfer-waste/", json=transfer_request)
    assert response.status_code == 404
    assert response.json() == {"detail": "Organization not found"}


@pytest.mark.asyncio
async def test_storage_not_found(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=1)]
    )
    mock_storage_gateway.get_storage_by_id.return_value = None
    transfer_request = {
        "waste_type": "BIO_WASTE",
        "amount": 1
    }
    response = client.post("/organizations/1/storages/1/transfer-waste/", json=transfer_request)
    assert response.status_code == 404
    assert response.json() == {"detail": "Storage not found"}


@pytest.mark.asyncio
async def test_storage_does_not_support_waste_type(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=1)]
    )
    mock_storage_gateway.get_storage_by_id.return_value = Storage(
        id=2,
        name="S2",
        location_x=100,
        location_y=0,
        capacities=[],
        current_levels=[]
    )
    transfer_request = {
        "waste_type": "BIO_WASTE",
        "amount": 1
    }
    response = client.post("/organizations/1/storages/2/transfer-waste/", json=transfer_request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Storage 2 does not support waste type BIO_WASTE."}


@pytest.mark.asyncio
async def test_storage_insufficient_capacity(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=2)]
    )
    mock_storage_gateway.get_storage_by_id.return_value = Storage(
        id=2,
        name="S2",
        location_x=100,
        location_y=0,
        capacities=[StorageCapacity(waste_type=WasteType.BIO_WASTE, capacity=1)],
        current_levels=[StorageCurrentLevel(waste_type=WasteType.BIO_WASTE, current_amount=1)]
    )
    transfer_request = {
        "waste_type": "BIO_WASTE",
        "amount": 2
    }
    response = client.post("/organizations/1/storages/2/transfer-waste/", json=transfer_request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Storage 2 does not have sufficient capacity for 2 of waste type BIO_WASTE."}


@pytest.mark.asyncio
async def test_organization_does_not_generate_waste_type(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[]
    )
    mock_storage_gateway.get_storage_by_id.return_value = Storage(
        id=2,
        name="S2",
        location_x=100,
        location_y=0,
        capacities=[StorageCapacity(waste_type=WasteType.BIO_WASTE, capacity=2)],
        current_levels=[StorageCurrentLevel(waste_type=WasteType.BIO_WASTE, current_amount=1)]
    )
    transfer_request = {
        "waste_type": "BIO_WASTE",
        "amount": 1
    }
    response = client.post("/organizations/1/storages/2/transfer-waste/", json=transfer_request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Organization 1 does not generate waste type BIO_WASTE."}


@pytest.mark.asyncio
async def test_organization_insufficient_waste(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=1)]
    )
    mock_storage_gateway.get_storage_by_id.return_value = Storage(
        id=2,
        name="S2",
        location_x=100,
        location_y=0,
        capacities=[StorageCapacity(waste_type=WasteType.BIO_WASTE, capacity=5)],
        current_levels=[StorageCurrentLevel(waste_type=WasteType.BIO_WASTE, current_amount=1)]
    )
    transfer_request = {
        "waste_type": "BIO_WASTE",
        "amount": 2
    }
    response = client.post("/organizations/1/storages/2/transfer-waste/", json=transfer_request)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Organization 1 has insufficient waste of type BIO_WASTE. Available: 1, Requested: 2."}
