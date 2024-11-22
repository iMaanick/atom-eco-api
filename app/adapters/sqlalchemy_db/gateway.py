from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.sqlalchemy_db import models
from app.application.models import Organization, OrganizationCreate, WasteType
from app.application.models.storage import Storage, StorageCreate
from app.application.protocols.database import OrganizationDatabaseGateway, StorageDatabaseGateway


class OrganizationSqlaGateway(OrganizationDatabaseGateway):
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

    async def delete_organization_by_id(self, organization_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(models.Organization).where(models.Organization.id == organization_id))
        organization = result.scalars().first()
        if not organization:
            return None
        await self.session.delete(organization)
        return organization.id

    async def update_organization_by_id(self, organization_id: int, organization_data: OrganizationCreate) -> Optional[
        int]:
        result = await self.session.execute(
            select(models.Organization).
            where(models.Organization.id == organization_id
                  ).options(selectinload(models.Organization.generated_waste))
        )
        organization = result.scalars().first()
        if not organization:
            return None
        organization.name = organization_data.name
        organization.location_x = organization_data.location_x
        organization.location_y = organization_data.location_y
        organization.generated_waste = [
            models.OrganizationWaste(waste_type=w.waste_type, amount=w.amount) for w in
            organization_data.generated_waste
        ]
        return organization.id

    async def reduce_organization_waste(self, organization_id: int, waste_type: WasteType, amount: float) -> None:
        organization_waste = await self.session.execute(
            select(models.OrganizationWaste)
            .where(models.OrganizationWaste.organization_id == organization_id)
            .where(models.OrganizationWaste.waste_type == waste_type)
        )
        organization_waste = organization_waste.scalars().first()

        organization_waste.amount -= amount

        await self.session.flush()

    async def generate_waste(self, organization_id: int, waste_type: WasteType, amount: float) -> None:
        organization_waste = await self.session.execute(
            select(models.OrganizationWaste)
            .where(models.OrganizationWaste.organization_id == organization_id)
            .where(models.OrganizationWaste.waste_type == waste_type)
        )
        organization_waste = organization_waste.scalars().first()

        organization_waste.amount += amount


class StorageSqlaGateway(StorageDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_storages(self) -> list[Storage]:
        query = select(models.Storage).options(
            selectinload(models.Storage.capacities)
        ).options(
            selectinload(models.Storage.current_levels))
        result = await self.session.execute(query)
        storage_list = [Storage.model_validate(storage) for storage in result.scalars().all()]
        return storage_list

    async def get_storage_by_id(self, storage_id: int) -> Optional[Storage]:
        query = select(models.Storage).where(models.Storage.id == storage_id).options(
            selectinload(models.Storage.capacities)
        ).options(
            selectinload(models.Storage.current_levels))
        result = await self.session.execute(query)
        storage = result.scalars().first()
        return Storage.model_validate(storage) if storage else None

    async def create_storage(self, storage_data: StorageCreate) -> int:
        new_storage = models.Storage(
            name=storage_data.name,
            location_x=storage_data.location_x,
            location_y=storage_data.location_y,
            capacities=[
                models.StorageCapacity(
                    waste_type=waste_item.waste_type,
                    capacity=waste_item.capacity
                )
                for waste_item in storage_data.capacities
            ],
            current_levels=[
                models.StorageCurrentLevel(
                    waste_type=waste_item.waste_type,
                    current_amount=waste_item.current_amount
                )
                for waste_item in storage_data.current_levels
            ]

        )
        self.session.add(new_storage)
        await self.session.flush()
        return new_storage.id

    async def update_storage_by_id(self, storage_id: int, storage_data: StorageCreate) -> Optional[int]:
        result = await self.session.execute(
            select(models.Storage).
            where(models.Storage.id == storage_id
                  ).options(
                selectinload(models.Storage.capacities)
            ).options(
                selectinload(models.Storage.current_levels)
            )
        )
        storage = result.scalars().first()
        if not storage:
            return None
        storage.name = storage_data.name
        storage.location_x = storage_data.location_x
        storage.location_y = storage_data.location_y
        storage.capacities = [
            models.StorageCapacity(
                waste_type=waste_item.waste_type,
                capacity=waste_item.capacity
            )
            for waste_item in storage_data.capacities
        ]
        storage.current_levels = [
            models.StorageCurrentLevel(
                waste_type=waste_item.waste_type,
                current_amount=waste_item.current_amount
            )
            for waste_item in storage_data.current_levels
        ]
        return storage.id

    async def delete_storage_by_id(self, storage_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(models.Storage).where(models.Storage.id == storage_id))
        storage = result.scalars().first()
        if not storage:
            return None
        await self.session.delete(storage)
        return storage.id

    async def add_waste_to_storage(self, storage_id: int, waste_type: WasteType, amount: float) -> None:
        storage_level = await self.session.execute(
            select(models.StorageCurrentLevel)
            .where(models.StorageCurrentLevel.storage_id == storage_id)
            .where(models.StorageCurrentLevel.waste_type == waste_type)
        )
        storage_level = storage_level.scalars().first()

        storage_level.current_amount += amount

        await self.session.flush()
