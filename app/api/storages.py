from typing import Annotated

from fastapi import APIRouter, Depends

from app.adapters.sqlalchemy_db.gateway import StorageSqlaGateway
from app.api.depends_stub import Stub
from app.application.models.storage import Storage
from app.application.protocols.database import StorageDatabaseGateway
from app.application.storages import get_storages_data

storages_router = APIRouter()


@storages_router.get("/", response_model=list[Storage])
async def get_storages(
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
) -> list[Storage]:
    storage_list = await get_storages_data(database)
    return storage_list
