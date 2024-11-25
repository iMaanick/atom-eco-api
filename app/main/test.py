import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.adapters.sqlalchemy_db.models import Organization, Storage
from app.adapters.sqlalchemy_db.models.organization_waste import OrganizationWaste
from app.adapters.sqlalchemy_db.models.storage_capacity import StorageCapacity
from app.adapters.sqlalchemy_db.models.storage_current_level import StorageCurrentLevel
from app.adapters.sqlalchemy_db.models.waste_type import WasteTypeEnum


def create_async_session(db_uri: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(db_uri, echo=False)
    return async_sessionmaker(bind=engine, class_=AsyncSession)


async def populate_test_data(session: AsyncSession) -> None:
    organizations_data = [
        {
            "name": "ОО 1",
            "location_x": 0,
            "location_y": 0,
            "generated_waste": [
                {"waste_type": WasteTypeEnum.PLASTIC, "amount": 10},
                {"waste_type": WasteTypeEnum.GLASS, "amount": 50},
                {"waste_type": WasteTypeEnum.BIO_WASTE, "amount": 50},
            ],
        },
        {
            "name": "ОО 2",
            "location_x": 0,
            "location_y": 0,
            "generated_waste": [
                {"waste_type": WasteTypeEnum.PLASTIC, "amount": 60},
                {"waste_type": WasteTypeEnum.GLASS, "amount": 20},
                {"waste_type": WasteTypeEnum.BIO_WASTE, "amount": 50},
            ],
        },
    ]

    storages_data = [
        {
            "name": "МНО 1",
            "location_x": 100,
            "location_y": 0,
            "capacities": [
                {"waste_type": WasteTypeEnum.GLASS, "capacity": 300},
                {"waste_type": WasteTypeEnum.PLASTIC, "capacity": 100},
            ],
            "current_levels": [
                {"waste_type": WasteTypeEnum.GLASS, "current_amount": 0},
                {"waste_type": WasteTypeEnum.PLASTIC, "current_amount": 0},
            ],
        },
        {
            "name": "МНО 2",
            "location_x": 50,
            "location_y": 50,
            "capacities": [
                {"waste_type": WasteTypeEnum.PLASTIC, "capacity": 50},
                {"waste_type": WasteTypeEnum.BIO_WASTE, "capacity": 150},
            ],
            "current_levels": [
                {"waste_type": WasteTypeEnum.PLASTIC, "current_amount": 0},
                {"waste_type": WasteTypeEnum.BIO_WASTE, "current_amount": 0},
            ],
        },
    ]

    for org_data in organizations_data:
        org = Organization(
            name=org_data["name"],
            location_x=org_data["location_x"],
            location_y=org_data["location_y"],
        )
        for waste in org_data["generated_waste"]:
            org.generated_waste.append(
                OrganizationWaste(
                    waste_type=waste["waste_type"], amount=waste["amount"]
                )
            )
        session.add(org)

    for storage_data in storages_data:
        storage = Storage(
            name=storage_data["name"],
            location_x=storage_data["location_x"],
            location_y=storage_data["location_y"],
        )
        for capacity in storage_data["capacities"]:
            storage.capacities.append(
                StorageCapacity(
                    waste_type=capacity["waste_type"], capacity=capacity["capacity"]
                )
            )
        for level in storage_data["current_levels"]:
            storage.current_levels.append(
                StorageCurrentLevel(
                    waste_type=level["waste_type"], current_amount=level["current_amount"]
                )
            )
        session.add(storage)

    await session.commit()


async def main() -> None:
    db_uri = os.getenv("DATABASE_URI")
    if not db_uri:
        raise ValueError("DATABASE_URI environment variable is not set")
    async_session_factory = create_async_session(db_uri)
    async with async_session_factory() as session:
        async with session.begin():
            await populate_test_data(session)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
