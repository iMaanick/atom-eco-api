from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.protocols.database import OrganizationDatabaseGateway, UoW
from app.main import init_routers


@pytest.fixture
def mock_organization_gateway():
    mock = AsyncMock(OrganizationDatabaseGateway)
    return mock


@pytest.fixture
def mock_uow() -> UoW:
    uow = AsyncMock()
    uow.commit = AsyncMock()
    uow.flush = AsyncMock()
    return uow


@pytest.fixture
def client(mock_organization_gateway):
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[OrganizationDatabaseGateway] = lambda: mock_organization_gateway
    app.dependency_overrides[UoW] = lambda: mock_uow

    return TestClient(app)
