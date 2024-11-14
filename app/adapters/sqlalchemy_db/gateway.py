from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.sqlalchemy_db import models
from app.application.models import Organization
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

    async def get_storages(self) -> list[Storage]:
        query = select(models.Storage).options(
            selectinload(models.Storage.capacities)
        ).options(
            selectinload(models.Storage.current_levels))
        result = await self.session.execute(query)
        storage_list = [Storage.model_validate(storage) for storage in result.scalars().all()]
        return storage_list
