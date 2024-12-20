from abc import ABC, abstractmethod
from typing import Optional

from app.application.models import Organization, OrganizationCreate, WasteType
from app.application.models.storage import Storage, StorageCreate


class UoW(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError


class OrganizationDatabaseGateway(ABC):

    @abstractmethod
    async def get_organizations(self) -> list[Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_organization_by_id(self, organization_id: int) -> Optional[Organization]:
        raise NotImplementedError

    @abstractmethod
    async def create_organization(self, organization_data: OrganizationCreate) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_organization_by_id(self, organization_id: int) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def update_organization_by_id(self, organization_id: int, organization_data: OrganizationCreate) -> Optional[
        int]:
        raise NotImplementedError

    @abstractmethod
    async def reduce_organization_waste(self, organization_id: int, waste_type: WasteType, amount: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def generate_waste(self, organization_id: int, waste_type: WasteType, amount: int) -> None:
        raise NotImplementedError


class StorageDatabaseGateway(ABC):

    @abstractmethod
    async def get_storages(self) -> list[Storage]:
        raise NotImplementedError

    @abstractmethod
    async def get_storage_by_id(self, storage_id: int) -> Optional[Storage]:
        raise NotImplementedError

    @abstractmethod
    async def create_storage(self, storage_data: StorageCreate) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_storage_by_id(self, storage_id: int, storage_data: StorageCreate) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def delete_storage_by_id(self, storage_id: int) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def add_waste_to_storage(self, storage_id: int, waste_type: WasteType, amount: int) -> None:
        raise NotImplementedError
