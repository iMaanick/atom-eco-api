from pydantic import BaseModel, ConfigDict

from app.application.models import WasteType


class StorageCapacity(BaseModel):
    waste_type: WasteType
    capacity: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
