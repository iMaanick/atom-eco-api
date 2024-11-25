from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.application.models import OrganizationWaste, WasteType, Organization
from app.application.models.storage import Storage
from app.application.models.storage_capacity import StorageCapacity
from app.application.models.storage_current_level import StorageCurrentLevel


@pytest.mark.asyncio
async def test_get_available_storages(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[
            OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=1)
        ]
    )
    mock_storage_gateway.get_storages.return_value = [
        Storage(
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
        ),
        Storage(
            id=3,
            name="S3",
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
                    current_amount=2
                )
            ]
        )
    ]

    response = client.get("/organizations/1/available-storages/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["capacities"][0]["waste_type"] == "BIO_WASTE"
    assert response.json()[0]["capacities"][0]["capacity"] == 2
    assert response.json()[0]["current_levels"][0]["waste_type"] == "BIO_WASTE"
    assert response.json()[0]["current_levels"][0]["current_amount"] == 1


@pytest.mark.asyncio
async def test_get_available_storages_no_suitable(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[
            OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=10)
        ]
    )
    mock_storage_gateway.get_storages.return_value = [
        Storage(
            id=2,
            name="S2",
            location_x=100,
            location_y=0,
            capacities=[
                StorageCapacity(
                    waste_type=WasteType.BIO_WASTE,
                    capacity=18
                )
            ],
            current_levels=[
                StorageCurrentLevel(
                    waste_type=WasteType.BIO_WASTE,
                    current_amount=10
                )
            ]
        ),
        Storage(
            id=3,
            name="S3",
            location_x=100,
            location_y=0,
            capacities=[
                StorageCapacity(
                    waste_type=WasteType.GLASS,
                    capacity=2000
                )
            ],
            current_levels=[
                StorageCurrentLevel(
                    waste_type=WasteType.GLASS,
                    current_amount=200
                )
            ]
        )
    ]

    response = client.get("/organizations/1/available-storages/")

    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_get_available_storages_several_waste_types(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = Organization(
        id=1,
        name="Org 1",
        location_x=0,
        location_y=0,
        generated_waste=[
            OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=10),
            OrganizationWaste(waste_type=WasteType.GLASS, amount=20)

        ]
    )
    mock_storage_gateway.get_storages.return_value = [
        Storage(
            id=2,
            name="S2",
            location_x=100,
            location_y=0,
            capacities=[
                StorageCapacity(
                    waste_type=WasteType.BIO_WASTE,
                    capacity=200
                )
            ],
            current_levels=[
                StorageCurrentLevel(
                    waste_type=WasteType.BIO_WASTE,
                    current_amount=10
                )
            ]
        ),
        Storage(
            id=3,
            name="S3",
            location_x=100,
            location_y=0,
            capacities=[
                StorageCapacity(
                    waste_type=WasteType.GLASS,
                    capacity=2000
                )
            ],
            current_levels=[
                StorageCurrentLevel(
                    waste_type=WasteType.GLASS,
                    current_amount=200
                )
            ]
        ),
        Storage(
            id=4,
            name="S4",
            location_x=100,
            location_y=0,
            capacities=[
                StorageCapacity(
                    waste_type=WasteType.BIO_WASTE,
                    capacity=2000
                ),
                StorageCapacity(
                    waste_type=WasteType.GLASS,
                    capacity=2000
                )
            ],
            current_levels=[
                StorageCurrentLevel(
                    waste_type=WasteType.BIO_WASTE,
                    current_amount=20
                ),
                StorageCurrentLevel(
                    waste_type=WasteType.GLASS,
                    current_amount=200
                )
            ]
        ),
    ]

    response = client.get("/organizations/1/available-storages/")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_available_storages_organization_not_found(
        client: TestClient,
        mock_organization_gateway: AsyncMock,
        mock_storage_gateway: AsyncMock
) -> None:
    mock_organization_gateway.get_organization_by_id.return_value = None

    response = client.get("/organizations/1/available-storages/")

    assert response.status_code == 404
    assert len(response.json()) == 1
    assert response.json()["detail"] == "Organization not found"
