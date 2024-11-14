from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.sqlalchemy_db.models import Base

from typing import TYPE_CHECKING

from .waste_type import WasteTypeEnum

if TYPE_CHECKING:
    from .organization import Organization


class OrganizationWaste(Base):
    __tablename__ = 'organization_waste'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    waste_type: Mapped[WasteTypeEnum] = mapped_column(Enum(WasteTypeEnum))
    amount: Mapped[int] = mapped_column(Integer)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="generated_waste")
