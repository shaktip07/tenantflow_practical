from pydantic import BaseModel


class OrganizationCreateSchema(BaseModel):
    organization_name: str
    email: str
    password: str


class OrganizationListingSchema(BaseModel):
    id: int
    name: str
    password: str
    host_name: str
    port: int

    class Config:
        from_attributes = True
