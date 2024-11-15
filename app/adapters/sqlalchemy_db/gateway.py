from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.sqlalchemy_db import models
from app.application.models import Organization, OrganizationCreate
from app.application.models.storage import Storage
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_organizations(self) -> list[Organization]:
        query = select(models.Organization).options(selectinload(models.Organization.generated_waste))
        result = await self.session.execute(query)
        organization_list = [Organization.model_validate(organization) for organization in result.scalars().all()]
        return organization_list

    async def get_organization_by_id(self, organization_id: int) -> Optional[Organization]:
        query = select(models.Organization).where(models.Organization.id == organization_id).options(
            selectinload(models.Organization.generated_waste))
        result = await self.session.execute(query)
        organization = result.scalars().first()
        if organization:
            return Organization.model_validate(organization)
        return None

    async def create_organization(self, organization_data: OrganizationCreate) -> int:
        new_organization = models.Organization(
            name=organization_data.name,
            location_x=organization_data.location_x,
            location_y=organization_data.location_y,
            generated_waste=[
                models.OrganizationWaste(
                    waste_type=waste_item.waste_type,
                    amount=waste_item.amount
                )
                for waste_item in organization_data.generated_waste
            ]
        )
        self.session.add(new_organization)
        await self.session.flush()
        return new_organization.id

    async def get_storages(self) -> list[Storage]:
        query = select(models.Storage).options(
            selectinload(models.Storage.capacities)
        ).options(
            selectinload(models.Storage.current_levels))
        result = await self.session.execute(query)
        storage_list = [Storage.model_validate(storage) for storage in result.scalars().all()]
        return storage_list
