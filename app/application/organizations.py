from app.application.models import Organization
from app.application.protocols.database import DatabaseGateway


async def get_organizations_data(
        database: DatabaseGateway,
) -> list[Organization]:
    organization_list = await database.get_organizations()
    return organization_list
