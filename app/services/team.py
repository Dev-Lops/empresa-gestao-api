import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.team import TeamRepository
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate


class TeamService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TeamRepository(db)

    async def get_all(self, company_id: uuid.UUID) -> list[TeamResponse]:
        teams = await self.repo.get_all(company_id)
        return [TeamResponse.model_validate(t) for t in teams]

    async def get_by_id(self, team_id: uuid.UUID) -> TeamResponse:
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipe não encontrada.",
            )
        return TeamResponse.model_validate(team)

    async def create(self, data: TeamCreate) -> TeamResponse:
        team = await self.repo.create(data)
        return TeamResponse.model_validate(team)

    async def update(self, team_id: uuid.UUID, data: TeamUpdate) -> TeamResponse:
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipe não encontrada.",
            )
        team = await self.repo.update(team, data)
        return TeamResponse.model_validate(team)

    async def delete(self, team_id: uuid.UUID) -> None:
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipe não encontrada.",
            )
        await self.repo.delete(team)