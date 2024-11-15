from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.sqlalchemy_db.models import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .organization_waste import OrganizationWaste


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    location_x: Mapped[float] = mapped_column(Float)
    location_y: Mapped[float] = mapped_column(Float)

    generated_waste: Mapped[list["OrganizationWaste"]] = relationship(
        "OrganizationWaste", back_populates="organization", cascade="all, delete-orphan"
    )
