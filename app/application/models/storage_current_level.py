from pydantic import BaseModel, ConfigDict

from app.application.models import WasteType


class StorageCurrentLevel(BaseModel):
    waste_type: WasteType
    current_amount: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
