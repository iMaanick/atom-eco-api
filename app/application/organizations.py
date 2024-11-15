from typing import Optional

from app.application.models import Organization
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
