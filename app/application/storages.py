from typing import Optional

from app.adapters.sqlalchemy_db.gateway import StorageSqlaGateway
from app.application.models.storage import Storage
from app.application.protocols.database import StorageDatabaseGateway


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
