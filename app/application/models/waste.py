from enum import Enum


class WasteType(str, Enum):
    BIO_WASTE = "BIO_WASTE"
    GLASS = "GLASS"
    PLASTIC = "PLASTIC"
