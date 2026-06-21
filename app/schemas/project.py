import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.project import ProjectStatus


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    company_id: uuid.UUID
    team_id: uuid.UUID | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
    team_id: uuid.UUID | None = None


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    status: ProjectStatus
    company_id: uuid.UUID
    team_id: uuid.UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}