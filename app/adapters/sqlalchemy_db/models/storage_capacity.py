from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.sqlalchemy_db.models import Base
from .waste_type import WasteTypeEnum

if TYPE_CHECKING:
    from .storage import Storage


class StorageCapacity(Base):
    __tablename__ = 'storage_capacities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    storage_id: Mapped[int] = mapped_column(ForeignKey('storages.id'))
    waste_type: Mapped[WasteTypeEnum] = mapped_column(Enum(WasteTypeEnum))
    capacity: Mapped[int] = mapped_column(Integer)

    storage: Mapped["Storage"] = relationship("Storage", back_populates="capacities")
