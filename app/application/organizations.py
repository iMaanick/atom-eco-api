import math
from typing import Optional

from app.application.models import Organization, OrganizationCreate
from app.application.protocols.database import OrganizationDatabaseGateway, UoW, StorageDatabaseGateway


async def get_organizations_data(
        database: OrganizationDatabaseGateway,
) -> list[Organization]:
    organization_list = await database.get_organizations()
    return organization_list


async def get_organization_data(
        organization_id: int,
        database: OrganizationDatabaseGateway,
) -> Optional[Organization]:
    organization = await database.get_organization_by_id(organization_id)
    return organization


async def add_organization(
        organization_data: OrganizationCreate,
        database: OrganizationDatabaseGateway,
        uow: UoW,
) -> int:
    organization_id = await database.create_organization(organization_data)
    await uow.commit()
    return organization_id


async def delete_organization(
        organization_id: int,
        database: OrganizationDatabaseGateway,
        uow: UoW,
) -> Optional[int]:
    organization_id = await database.delete_organization_by_id(organization_id)
    await uow.commit()
    return organization_id


async def update_organization_by_id(
        organization_id: int,
        organization_data: OrganizationCreate,
        database: OrganizationDatabaseGateway,
        uow: UoW,
) -> int:
    organization_id = await database.update_organization_by_id(organization_id, organization_data)
    await uow.commit()
    return organization_id


async def calculate_distance_to_storage(
        organization_id: int,
        storage_id: int,
        organization_database: OrganizationDatabaseGateway,
        storage_database: StorageDatabaseGateway,

) -> Optional[float]:
    organization = await organization_database.get_organization_by_id(organization_id)
    storage = await storage_database.get_storage_by_id(storage_id)
    if organization is None or storage is None:
        return None
    return math.sqrt(
        (organization.location_x - storage.location_x) ** 2 + (organization.location_y - storage.location_y) ** 2
    )
