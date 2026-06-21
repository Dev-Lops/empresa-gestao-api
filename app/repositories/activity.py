import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, project_id: uuid.UUID) -> list[Activity]:
        result = await self.db.execute(
            select(Activity).where(Activity.project_id == project_id)
        )
        return list(result.scalars().all())

    async def get_by_id(self, activity_id: uuid.UUID) -> Activity | None:
        result = await self.db.execute(
            select(Activity).where(Activity.id == activity_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: ActivityCreate) -> Activity:
        activity = Activity(**data.model_dump())
        self.db.add(activity)
        await self.db.flush()
        await self.db.refresh(activity)
        return activity

    async def update(self, activity: Activity, data: ActivityUpdate) -> Activity:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(activity, field, value)
        await self.db.flush()
        await self.db.refresh(activity)
        return activity

    async def delete(self, activity: Activity) -> None:
        await self.db.delete(activity)
        await self.db.flush()