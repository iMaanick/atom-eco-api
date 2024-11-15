from typing import Optional

from app.application.models import Organization, OrganizationCreate
from app.application.protocols.database import DatabaseGateway, UoW


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
        uow: UoW,
) -> int:
    organization_id = await database.create_organization(organization_data)
    await uow.commit()
    return organization_id


async def delete_organization(
        organization_id: int,
        database: DatabaseGateway,
        uow: UoW,
) -> Optional[int]:
    organization_id = await database.delete_organization_by_id(organization_id)
    await uow.commit()
    return organization_id
