from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.adapters.sqlalchemy_db.gateway import StorageSqlaGateway
from app.api.depends_stub import Stub
from app.application.models.storage import Storage
from app.application.protocols.database import StorageDatabaseGateway
from app.application.storages import get_storages_data, get_storage_data

storages_router = APIRouter()


@storages_router.get("/", response_model=list[Storage])
async def get_storages(
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
) -> list[Storage]:
    storage_list = await get_storages_data(database)
    return storage_list


@storages_router.get("/{storage_id}/", response_model=Storage)
async def get_storage(
        storage_id: int,
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
) -> Storage:
    storage = await get_storage_data(storage_id, database)
    if not storage:
        raise HTTPException(status_code=404, detail="Storage not found")
    return storage
