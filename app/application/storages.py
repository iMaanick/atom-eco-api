from app.adapters.sqlalchemy_db.gateway import StorageSqlaGateway
from app.application.models.storage import Storage
from app.application.protocols.database import StorageDatabaseGateway


async def get_storages_data(
        database: StorageDatabaseGateway,
) -> list[Storage]:
    storage_list = await database.get_storages()
    return storage_list
