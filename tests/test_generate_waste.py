import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_generate_waste(client: TestClient, mock_organization_gateway, mock_uow):
    mock_organization_gateway.generate_waste.return_value = None
    params = {
        "waste_type": "BIO_WASTE",
        "amount": 50
    }
    response = client.get(f"/organizations/1/generate_waste/", params=params)

    assert response.status_code == 200
    assert response.json() == {"detail": f"Successfully added 50 of BIO_WASTE waste to organization 1."}

    mock_organization_gateway.generate_waste.assert_called_once_with(1, "BIO_WASTE", 50)
