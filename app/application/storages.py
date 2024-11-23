from typing import Optional

from app.application.models.storage import Storage, StorageCreate
from app.application.protocols.database import StorageDatabaseGateway, UoW


async def get_storages_data(
        database: StorageDatabaseGateway,
) -> list[Storage]:
    storage_list = await database.get_storages()
    return storage_list


async def get_storage_data(
        storage_id: int,
        database: StorageDatabaseGateway,
) -> Optional[Storage]:
    storage = await database.get_storage_by_id(storage_id)
    return storage


async def add_storage(
        organization_data: StorageCreate,
        database: StorageDatabaseGateway,
        uow: UoW,
) -> int:
    storage_id = await database.create_storage(organization_data)
    await uow.commit()
    return storage_id


async def update_storage_by_id(
        storage_id: int,
        storage_data: StorageCreate,
        database: StorageDatabaseGateway,
        uow: UoW,
) -> int:
    storage_id = await database.update_storage_by_id(storage_id, storage_data)
    await uow.commit()
    return storage_id


async def delete_storage_by_id(
        organization_id: int,
        database: StorageDatabaseGateway,
        uow: UoW,
) -> Optional[int]:
    organization_id = await database.delete_storage_by_id(organization_id)
    await uow.commit()
    return organization_id
