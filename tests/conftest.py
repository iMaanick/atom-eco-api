from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.protocols.database import OrganizationDatabaseGateway, UoW, StorageDatabaseGateway
from app.main import init_routers


@pytest.fixture
def mock_organization_gateway() -> OrganizationDatabaseGateway:
    mock = AsyncMock(OrganizationDatabaseGateway)
    return mock


@pytest.fixture
def mock_storage_gateway() -> StorageDatabaseGateway:
    mock = AsyncMock(StorageDatabaseGateway)
    return mock


@pytest.fixture
def mock_uow() -> UoW:
    uow = AsyncMock()
    uow.commit = AsyncMock()
    uow.flush = AsyncMock()
    return uow


@pytest.fixture
def client(mock_organization_gateway: AsyncMock, mock_storage_gateway: AsyncMock, mock_uow: AsyncMock) -> TestClient:
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[OrganizationDatabaseGateway] = lambda: mock_organization_gateway
    app.dependency_overrides[StorageDatabaseGateway] = lambda: mock_storage_gateway
    app.dependency_overrides[UoW] = lambda: mock_uow

    return TestClient(app)
