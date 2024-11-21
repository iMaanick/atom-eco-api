from typing import List

from pydantic import BaseModel, ConfigDict

from app.application.models.organization_waste import OrganizationWaste


class Organization(BaseModel):
    id: int
    name: str
    location_x: float
    location_y: float
    generated_waste: List[OrganizationWaste]
    model_config = ConfigDict(from_attributes=True)


class OrganizationCreate(BaseModel):
    name: str
    location_x: float
    location_y: float
    generated_waste: List[OrganizationWaste]


class OrganizationCreateResponse(BaseModel):
    organization_id: int


class DeleteOrganizationResponse(BaseModel):
    detail: str


class UpdateOrganizationResponse(BaseModel):
    detail: str


class DistanceResponse(BaseModel):
    distance: float

