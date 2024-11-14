from enum import Enum

from pydantic import BaseModel


class WasteType(str, Enum):
    BIO_WASTE = "bio_waste"
    GLASS = "glass"
    PLASTIC = "plastic"
