import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


class TeamRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, company_id: uuid.UUID) -> list[Team]:
        result = await self.db.execute(
            select(Team).where(Team.company_id == company_id)
        )
        return list(result.scalars().all())

    async def get_by_id(self, team_id: uuid.UUID) -> Team | None:
        result = await self.db.execute(
            select(Team).where(Team.id == team_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: TeamCreate) -> Team:
        team = Team(**data.model_dump())
        self.db.add(team)
        await self.db.flush()
        await self.db.refresh(team)
        return team

    async def update(self, team: Team, data: TeamUpdate) -> Team:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(team, field, value)
        await self.db.flush()
        await self.db.refresh(team)
        return team

    async def delete(self, team: Team) -> None:
        await self.db.delete(team)
        await self.db.flush()