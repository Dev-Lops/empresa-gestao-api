import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.activity import ActivityRepository
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate


class ActivityService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ActivityRepository(db)

    async def get_all(self, project_id: uuid.UUID) -> list[ActivityResponse]:
        activities = await self.repo.get_all(project_id)
        return [ActivityResponse.model_validate(a) for a in activities]

    async def get_by_id(self, activity_id: uuid.UUID) -> ActivityResponse:
        activity = await self.repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atividade não encontrada.",
            )
        return ActivityResponse.model_validate(activity)

    async def create(self, data: ActivityCreate) -> ActivityResponse:
        activity = await self.repo.create(data)
        return ActivityResponse.model_validate(activity)

    async def update(
        self, activity_id: uuid.UUID, data: ActivityUpdate
    ) -> ActivityResponse:
        activity = await self.repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atividade não encontrada.",
            )
        activity = await self.repo.update(activity, data)
        return ActivityResponse.model_validate(activity)

    async def delete(self, activity_id: uuid.UUID) -> None:
        activity = await self.repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atividade não encontrada.",
            )
        await self.repo.delete(activity)