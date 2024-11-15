import enum


class WasteTypeEnum(str, enum.Enum):
    BIO_WASTE = "BIO_WASTE"
    GLASS = "GLASS"
    PLASTIC = "PLASTIC"
