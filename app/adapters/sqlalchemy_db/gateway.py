from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.sqlalchemy_db import models
from app.application.models.organization import Organization
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_organizations(self) -> list[Organization]:
        query = select(models.Organization).options(selectinload(models.Organization.generated_waste))
        result = await self.session.execute(query)
        organization_list = [Organization.model_validate(organization) for organization in result.scalars().all()]
        return organization_list
