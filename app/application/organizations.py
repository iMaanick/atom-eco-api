from typing import Optional

from app.application.models import Organization, OrganizationCreate
from app.application.protocols.database import DatabaseGateway


async def get_organizations_data(
        database: DatabaseGateway,
) -> list[Organization]:
    organization_list = await database.get_organizations()
    return organization_list


async def get_organization_data(
        organization_id: int,
        database: DatabaseGateway,
) -> Optional[Organization]:
    organization = await database.get_organization_by_id(organization_id)
    return organization


async def add_organization(
        organization_data: OrganizationCreate,
        database: DatabaseGateway,
) -> int:
    organization_id = await database.create_organization(organization_data)
    return organization_id
