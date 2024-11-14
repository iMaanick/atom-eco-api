import datetime
from abc import ABC, abstractmethod
from typing import Optional

from app.application.models.crypto_price import CryptoPrice, CryptoPriceCreate
from app.application.models.organization import Organization


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

