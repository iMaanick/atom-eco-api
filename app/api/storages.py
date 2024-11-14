from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.models.storage import Storage
from app.application.protocols.database import DatabaseGateway
from app.application.storages import get_storages_data

storages_router = APIRouter()


@storages_router.get("/", response_model=list[Storage])
async def get_storages(
        database: Annotated[DatabaseGateway, Depends()],
) -> list[Storage]:
    storage_list = await get_storages_data(database)
    return storage_list
