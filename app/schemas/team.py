import uuid
from datetime import datetime

from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    description: str | None = None
    company_id: uuid.UUID


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class TeamResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    is_active: bool
    company_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}