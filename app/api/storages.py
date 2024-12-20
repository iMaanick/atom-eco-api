from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.depends_stub import Stub
from app.application.models.storage import Storage, StorageCreate, StorageCreateResponse, UpdateStorageResponse, \
    DeleteStorageResponse
from app.application.protocols.database import StorageDatabaseGateway, UoW
from app.application.storages import get_storages_data, get_storage_data, add_storage, update_storage_by_id, \
    delete_storage_by_id

storages_router = APIRouter()


@storages_router.get("/", response_model=list[Storage])
async def get_storages(
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
) -> list[Storage]:
    """
    Retrieve a list of all storages.

    Returns:
        list[Storage]: A list of storage objects.
    """
    storage_list = await get_storages_data(database)
    return storage_list


@storages_router.get("/{storage_id}/", response_model=Storage)
async def get_storage(
        storage_id: int,
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
) -> Storage:
    """
    Retrieve a specific storage by its ID.

    Returns:
        Storage: The storage object corresponding to the specified ID.

    Raises:
        HTTPException: If the storage is not found.
    """
    storage = await get_storage_data(storage_id, database)
    if not storage:
        raise HTTPException(status_code=404, detail="Storage not found")
    return storage


@storages_router.post("/", response_model=StorageCreateResponse)
async def create_organization(
        organization_data: StorageCreate,
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
        uow: Annotated[UoW, Depends()],
) -> StorageCreateResponse:
    """
    Create a new storage.

    Returns:
        StorageCreateResponse: Response containing the ID of the newly created storage.
    """
    storage_id = await add_storage(organization_data, database, uow)
    return StorageCreateResponse(storage_id=storage_id)


@storages_router.put("/{storage_id}/", response_model=UpdateStorageResponse)
async def update_storage(
        storage_id: int,
        storage_data: StorageCreate,
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
        uow: Annotated[UoW, Depends()],
) -> UpdateStorageResponse:
    """
    Update an existing storage's details by its ID.

    Returns:
        UpdateStorageResponse: Response indicating that the storage was updated successfully.

    Raises:
        HTTPException: If the storage is not found.
    """
    updated_storage_id = await update_storage_by_id(storage_id, storage_data, database, uow)
    if not updated_storage_id:
        raise HTTPException(status_code=404, detail="Storage not found")
    return UpdateStorageResponse(detail="Storage updated successfully")


@storages_router.delete("/{storage_id}/", response_model=DeleteStorageResponse)
async def delete_storage(
        storage_id: int,
        database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
        uow: Annotated[UoW, Depends()],
) -> DeleteStorageResponse:
    """
    Delete a specific storage by its ID.

    Returns:
        DeleteStorageResponse: Response indicating whether the storage was successfully deleted.

    Raises:
        HTTPException: If the storage is not found.
    """
    deleted_storage_id = await delete_storage_by_id(storage_id, database, uow)
    if not deleted_storage_id:
        raise HTTPException(status_code=404, detail="Storage not found")
    return DeleteStorageResponse(detail="Storage deleted successfully")
