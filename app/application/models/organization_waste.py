from pydantic import BaseModel, ConfigDict

from app.application.models.waste import WasteType


class OrganizationWaste(BaseModel):
    waste_type: WasteType
    amount: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
