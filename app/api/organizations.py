from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.application.models import Organization, OrganizationCreate
from app.application.models.organization import OrganizationCreateResponse
from app.application.organizations import get_organizations_data, get_organization_data
from app.application.protocols.database import DatabaseGateway, UoW

organizations_router = APIRouter()


@organizations_router.get("/", response_model=list[Organization])
async def get_organizations(
        database: Annotated[DatabaseGateway, Depends()],
) -> list[Organization]:
    organization_list = await get_organizations_data(database)
    return organization_list


@organizations_router.get("/{organization_id}", response_model=Organization)
async def get_organizations(
        organization_id: int,
        database: Annotated[DatabaseGateway, Depends()],
) -> Organization:
    organization = await get_organization_data(organization_id, database)
    if not organization:
        raise HTTPException(status_code=404, detail="Data not found for specified organization_id.")
    return organization


@organizations_router.post("/", response_model=OrganizationCreateResponse)
async def create_organization(
        organization_data: OrganizationCreate,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> OrganizationCreateResponse:
    organization_id = await database.create_organization(organization_data)
    await uow.commit()
    return OrganizationCreateResponse(organization_id=organization_id)
