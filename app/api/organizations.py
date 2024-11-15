from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.models import Organization, OrganizationCreate, OrganizationCreateResponse, \
    DeleteOrganizationResponse, UpdateOrganizationResponse
from app.application.organizations import get_organizations_data, get_organization_data, add_organization, \
    delete_organization, update_organization_by_id
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
    organization_id = await add_organization(organization_data, database, uow)
    return OrganizationCreateResponse(organization_id=organization_id)


@organizations_router.delete("/", response_model=DeleteOrganizationResponse)
async def delete_organization_by_id(
        organization_id: int,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> DeleteOrganizationResponse:
    organization_id = await delete_organization(organization_id, database, uow)
    if not organization_id:
        raise HTTPException(status_code=404, detail="Organization not found")
    return DeleteOrganizationResponse(detail="Organization deleted successfully")


@organizations_router.put("/{organization_id}/", response_model=UpdateOrganizationResponse)
async def update_organization(
        organization_id: int,
        organization_data: OrganizationCreate,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> UpdateOrganizationResponse:
    organization_id = await update_organization_by_id(organization_id,
                                                      organization_data,
                                                      database,
                                                      uow)
    if not organization_id:
        raise HTTPException(status_code=404, detail="Organization not found")
    return UpdateOrganizationResponse(detail="Organization updated successfully")
