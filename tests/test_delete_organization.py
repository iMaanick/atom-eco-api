import pytest


@pytest.mark.asyncio
async def test_delete_organization(client, mock_organization_gateway):
    mock_organization_gateway.delete_organization_by_id.return_value = 1

    response = client.delete("/organizations/", params={"organization_id": 1})

    assert response.status_code == 200
    assert response.json()["detail"] == "Organization deleted successfully"


@pytest.mark.asyncio
async def test_delete_organization_not_found(client, mock_organization_gateway):
    mock_organization_gateway.delete_organization_by_id.return_value = None

    response = client.delete("/organizations/", params={"organization_id": 999})

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found"
