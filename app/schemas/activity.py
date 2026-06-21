import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.activity import ActivityPriority, ActivityStatus


class ActivityCreate(BaseModel):
    title: str
    description: str | None = None
    priority: ActivityPriority = ActivityPriority.MEDIUM
    project_id: uuid.UUID
    responsible_id: uuid.UUID | None = None


class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ActivityStatus | None = None
    priority: ActivityPriority | None = None
    responsible_id: uuid.UUID | None = None


class ActivityResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    status: ActivityStatus
    priority: ActivityPriority
    project_id: uuid.UUID
    responsible_id: uuid.UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}