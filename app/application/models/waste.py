from enum import Enum


class WasteType(str, Enum):
    BIO_WASTE = "bio_waste"
    GLASS = "glass"
    PLASTIC = "plastic"
