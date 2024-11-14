from abc import ABC, abstractmethod

from app.application.models import Organization
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
    async def get_storages(self) -> list[Storage]:
        raise NotImplementedError
