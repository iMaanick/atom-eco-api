from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.depends_stub import Stub
from app.application.models import Organization, OrganizationCreate, OrganizationCreateResponse, \
    DeleteOrganizationResponse, UpdateOrganizationResponse, OrganizationWaste
from app.application.models.organization import DistanceResponse
from app.application.models.storage import AvailableStorageResponse
from app.application.models.waste import WasteTransferResponse, WasteTransferRequest, WasteType, GenerateWasteResponse
from app.application.organizations import get_organizations_data, get_organization_data, add_organization, \
    delete_organization, update_organization_by_id, calculate_distance_to_storage, \
    get_available_storages_for_organization, has_sufficient_capacity, transfer_waste, organization_generate_waste
from app.application.protocols.database import OrganizationDatabaseGateway, UoW, StorageDatabaseGateway
from app.application.storages import get_storage_data

organizations_router = APIRouter()


@organizations_router.get("/", response_model=list[Organization])
async def get_organizations(
        database: Annotated[OrganizationDatabaseGateway, Depends()],
) -> list[Organization]:
    """
    Retrieve a list of all organizations.

    Returns:
        list[Organization]: A list of organization objects.
    """
    organization_list = await get_organizations_data(database)
    return organization_list


@organizations_router.get("/{organization_id}", response_model=Organization)
async def get_organization(
        organization_id: int,
        database: Annotated[OrganizationDatabaseGateway, Depends()],
) -> Organization:
    """
    Retrieve a single organization by its ID.

    Returns:
        Organization: The organization object corresponding to the specified ID.

    Raises:
        HTTPException: If the organization is not found.
    """
    organization = await get_organization_data(organization_id, database)
    if not organization:
        raise HTTPException(status_code=404, detail="Data not found for specified organization_id.")
    return organization


@organizations_router.post("/", response_model=OrganizationCreateResponse)
async def create_organization(
        organization_data: OrganizationCreate,
        database: Annotated[OrganizationDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> OrganizationCreateResponse:
    """
    Create a new organization.

    Returns:
        OrganizationCreateResponse: Response containing the ID of the newly created organization.
    """
    organization_id = await add_organization(organization_data, database, uow)
    return OrganizationCreateResponse(organization_id=organization_id)


@organizations_router.delete("/", response_model=DeleteOrganizationResponse)
async def delete_organization_by_id(
        organization_id: int,
        database: Annotated[OrganizationDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> DeleteOrganizationResponse:
    """
    Delete an organization by its ID.

    Returns:
        DeleteOrganizationResponse: Response indicating whether the organization was successfully deleted.

    Raises:
        HTTPException: If the organization is not found.
    """
    deleted_organization_id = await delete_organization(organization_id, database, uow)
    if not deleted_organization_id:
        raise HTTPException(status_code=404, detail="Organization not found")
    return DeleteOrganizationResponse(detail="Organization deleted successfully")


@organizations_router.put("/{organization_id}/", response_model=UpdateOrganizationResponse)
async def update_organization(
        organization_id: int,
        organization_data: OrganizationCreate,
        database: Annotated[OrganizationDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> UpdateOrganizationResponse:
    """
    Update an existing organization's details by its ID.

    Returns:
        UpdateOrganizationResponse: Response indicating that the organization was updated.

    Raises:
        HTTPException: If the organization is not found.
    """
    updated_organization_id = await update_organization_by_id(organization_id,
                                                              organization_data,
                                                              database,
                                                              uow)
    if not updated_organization_id:
        raise HTTPException(status_code=404, detail="Organization not found")
    return UpdateOrganizationResponse(detail="Organization updated successfully")


@organizations_router.get("/{organization_id}/distance-to-storage/{storage_id}/", response_model=DistanceResponse)
async def get_distance_to_storage(
        organization_id: int,
        storage_id: int,
        organization_database: Annotated[OrganizationDatabaseGateway, Depends()],
        storage_database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
) -> DistanceResponse:
    """
    Calculate the distance from an organization to a specific storage.

    Returns:
        DistanceResponse: The calculated distance between the organization and storage.

    Raises:
        HTTPException: If either the organization or storage is not found.
    """
    distance = await calculate_distance_to_storage(organization_id, storage_id, organization_database, storage_database)
    if distance is None:
        raise HTTPException(status_code=404, detail="Invalid organization or storage")
    return DistanceResponse(distance=distance)


@organizations_router.get("/{organization_id}/available-storages/", response_model=list[AvailableStorageResponse])
async def get_available_storages(
        organization_id: int,
        organization_database: Annotated[OrganizationDatabaseGateway, Depends()],
        storage_database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
) -> list[AvailableStorageResponse]:
    """
    Get a list of available storages for a specific organization.

    Returns:
        list[AvailableStorageResponse]: A list of available storages with details like distance and capacities.

    Raises:
        HTTPException: If the organization is not found.
    """
    organization = await get_organization_data(organization_id, organization_database)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    available_storages = await get_available_storages_for_organization(organization, storage_database)
    return available_storages


@organizations_router.post(
    "/{organization_id}/storages/{storage_id}/transfer-waste/",
    response_model=WasteTransferResponse
)
async def transfer_waste_to_specific_storage(
        organization_id: int,
        storage_id: int,
        transfer_request: WasteTransferRequest,
        organization_database: Annotated[OrganizationDatabaseGateway, Depends()],
        storage_database: Annotated[StorageDatabaseGateway, Depends(Stub(StorageDatabaseGateway))],
        uow: Annotated[UoW, Depends()]
) -> WasteTransferResponse:
    """
    Transfer waste from an organization to a specific storage.

    Returns:
        WasteTransferResponse: Response indicating the success of the waste transfer.

    Raises:
        HTTPException: If any validation fails (e.g., insufficient capacity, invalid waste type).
    """
    organization = await get_organization_data(organization_id, organization_database)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    storage = await get_storage_data(storage_id, storage_database)
    if not storage:
        raise HTTPException(status_code=404, detail="Storage not found")

    if not any(cap.waste_type == transfer_request.waste_type for cap in storage.capacities):
        raise HTTPException(
            status_code=400,
            detail=f"Storage {storage_id} does not support waste type {transfer_request.waste_type}."
        )

    if not has_sufficient_capacity(
            storage,
            [OrganizationWaste(waste_type=transfer_request.waste_type, amount=transfer_request.amount)]
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Storage {storage_id} does not have sufficient capacity for {transfer_request.amount} of "
                   f"waste type {transfer_request.waste_type}."
        )

    organization_waste = next(
        (w for w in organization.generated_waste if w.waste_type == transfer_request.waste_type),
        None
    )
    if not organization_waste:
        raise HTTPException(
            status_code=400,
            detail=f"Organization {organization_id} does not generate waste type {transfer_request.waste_type}."
        )

    if organization_waste.amount < transfer_request.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Organization {organization_id} has insufficient waste of type {transfer_request.waste_type}. "
                   f"Available: {organization_waste.amount}, Requested: {transfer_request.amount}."
        )
    await transfer_waste(
        organization_id,
        storage_id,
        transfer_request,
        organization_database,
        storage_database,
        uow
    )

    return WasteTransferResponse(
        detail="Waste transferred successfully."
    )


@organizations_router.get("/{organization_id}/generate_waste/", response_model=GenerateWasteResponse)
async def generate_waste(
        organization_id: int,
        waste_type: WasteType,
        amount: Annotated[int, Query(gt=0)],
        database: Annotated[OrganizationDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()]
) -> GenerateWasteResponse:
    """
    Generate a specific amount of waste for an organization.

    Returns:
        GenerateWasteResponse: Response indicating the successful generation of waste.

    Raises:
        HTTPException: If the organization is not found.
    """
    organization = await get_organization_data(organization_id, database)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    await organization_generate_waste(organization_id, waste_type, amount, database, uow)
    return GenerateWasteResponse(
        detail=f"Successfully added {amount} of {waste_type} waste to organization {organization_id}."
    )
