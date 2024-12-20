from pydantic import BaseModel, ConfigDict

from app.application.models.storage_capacity import StorageCapacity
from app.application.models.storage_current_level import StorageCurrentLevel


class Storage(BaseModel):
    id: int
    name: str
    location_x: float
    location_y: float
    capacities: list[StorageCapacity]
    current_levels: list[StorageCurrentLevel]
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class StorageCreate(BaseModel):
    name: str
    location_x: float
    location_y: float
    capacities: list[StorageCapacity]
    current_levels: list[StorageCurrentLevel]


class StorageCreateResponse(BaseModel):
    storage_id: int


class UpdateStorageResponse(BaseModel):
    detail: str


class DeleteStorageResponse(BaseModel):
    detail: str


class AvailableStorageResponse(BaseModel):
    storage_id: int
    name: str
    distance: float
    capacities: list[StorageCapacity]
    current_levels: list[StorageCurrentLevel]
