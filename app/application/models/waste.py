from enum import Enum

from pydantic import BaseModel, Field


class WasteType(str, Enum):
    BIO_WASTE = "BIO_WASTE"
    GLASS = "GLASS"
    PLASTIC = "PLASTIC"


class WasteTransferResponse(BaseModel):
    detail: str


class WasteTransferRequest(BaseModel):
    waste_type: WasteType = Field(..., description="The type of waste being transferred.")
    amount: int = Field(..., gt=0, description="The amount of waste to be transferred. Must be greater than 0.")


class GenerateWasteResponse(BaseModel):
    detail: str
