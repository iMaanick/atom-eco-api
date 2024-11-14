from fastapi import APIRouter

from .index import index_router
from .organizations import organizations_router
from .storages import storages_router

root_router = APIRouter()


root_router.include_router(
    organizations_router,
    prefix="/organizations",
    tags=["organizations"]
)
root_router.include_router(
    storages_router,
    prefix="/storages",
    tags=["storages"]
)
root_router.include_router(
    index_router,
)
