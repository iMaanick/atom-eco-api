from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.adapters.sqlalchemy_db.models import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .storage_capacity import StorageCapacity
    from .storage_current_level import StorageCurrentLevel


class Storage(Base):
    __tablename__ = 'storages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    location_x: Mapped[float] = mapped_column(Float)
    location_y: Mapped[float] = mapped_column(Float)

    capacities: Mapped[list["StorageCapacity"]] = relationship(
        "StorageCapacity", back_populates="storage", cascade="all, delete-orphan"
    )
    current_levels: Mapped[list["StorageCurrentLevel"]] = relationship(
        "StorageCurrentLevel", back_populates="storage", cascade="all, delete-orphan"
    )