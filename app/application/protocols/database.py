from abc import ABC, abstractmethod
from typing import Optional

from app.application.models import Organization, OrganizationCreate
from app.application.models.storage import Storage


class UoW(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError


class DatabaseGateway(ABC):

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


class StorageDatabaseGateway(ABC):

    @abstractmethod
    async def get_storages(self) -> list[Storage]:
        raise NotImplementedError
