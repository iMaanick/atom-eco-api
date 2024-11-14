from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.models.organization import Organization
from app.application.organizations import get_organizations_data
from app.application.protocols.database import DatabaseGateway

organizations_router = APIRouter()


@organizations_router.get("/", response_model=list[Organization])
async def get_organizations(
        database: Annotated[DatabaseGateway, Depends()],
) -> list[Organization]:

    organization_list = await get_organizations_data(database)
    return organization_list
