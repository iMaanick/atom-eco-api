from fastapi import APIRouter

from .index import index_router
from .organizations import organizations_router
root_router = APIRouter()


root_router.include_router(
    organizations_router,
    prefix="/organizations",
    tags=["organizations"]
)
root_router.include_router(
    index_router,
)
