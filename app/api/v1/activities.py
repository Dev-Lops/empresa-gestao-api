import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.schemas.user import UserResponse
from app.services.activity import ActivityService

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=list[ActivityResponse])
async def list_activities(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = ActivityService(db)
    return await service.get_all(project_id)


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = ActivityService(db)
    return await service.get_by_id(activity_id)


@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    data: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = ActivityService(db)
    return await service.create(data)


@router.patch("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: uuid.UUID,
    data: ActivityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = ActivityService(db)
    return await service.update(activity_id, data)


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = ActivityService(db)
    await service.delete(activity_id)