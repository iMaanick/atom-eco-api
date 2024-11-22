import pytest

from app.application.models import Organization, OrganizationWaste, WasteType


@pytest.mark.asyncio
async def test_get_organizations(client, mock_organization_gateway):
    mock_organization_gateway.get_organizations.return_value = [
        Organization(id=1, name="Org 1", location_x=0, location_y=0, generated_waste=[
            OrganizationWaste(waste_type=WasteType.BIO_WASTE, amount=1, )
        ]
                     ),
        Organization(id=12, name="Org 2", location_x=0, location_y=0, generated_waste=[
            OrganizationWaste(waste_type=WasteType.GLASS, amount=11, )
        ]
                     ),
    ]

    response = client.get("/organizations/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Org 1"
    assert response.json()[1]["name"] == "Org 2"


@pytest.mark.asyncio
async def test_get_organizations_empty(client, mock_organization_gateway):
    mock_organization_gateway.get_organizations.return_value = []

    response = client.get("/organizations/")

    assert response.status_code == 200
    assert len(response.json()) == 0
