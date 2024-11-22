import pytest


@pytest.mark.asyncio
async def test_create_organization(client, mock_organization_gateway, mock_uow):
    mock_organization_gateway.create_organization.return_value = 1

    organization_data = {
        "name": "New Org",
        "location_x": 0,
        "location_y": 0,
        "generated_waste": [
            {
                "waste_type": "BIO_WASTE",
                "amount": 25,
            }
        ]
    }

    response = client.post("/organizations/", json=organization_data)
    assert response.status_code == 200
    assert response.json()["organization_id"] == 1


@pytest.mark.asyncio
async def test_create_organization_unprocessable_entity(client, mock_organization_gateway, mock_uow):
    organization_data = {
        "name1": "New Org",
        "location_x": 0,
        "location_y": 0,
        "generated_waste": [
            {
                "waste_type": "BIO_WASTE",
                "amount": 25,
            }
        ]
    }

    response = client.post("/organizations/", json=organization_data)
    assert response.status_code == 422
