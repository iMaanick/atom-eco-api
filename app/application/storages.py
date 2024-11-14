from app.application.models.storage import Storage
from app.application.protocols.database import DatabaseGateway


async def get_storages_data(
        database: DatabaseGateway,
) -> list[Storage]:
    storage_list = await database.get_storages()
    return storage_list
