import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import check_same_company
from app.repositories.team import TeamRepository
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from app.schemas.user import UserResponse


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

    async def create(
        self, data: TeamCreate, current_user: UserResponse
    ) -> TeamResponse:
        # Garante que o usuário só cria equipes na sua própria empresa
        check_same_company(current_user.company_id, data.company_id)
        team = await self.repo.create(data)
        return TeamResponse.model_validate(team)

    async def update(
        self, team_id: uuid.UUID, data: TeamUpdate, current_user: UserResponse
    ) -> TeamResponse:
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipe não encontrada.",
            )
        # Garante que o usuário só edita equipes da sua empresa
        check_same_company(current_user.company_id, team.company_id)
        team = await self.repo.update(team, data)
        return TeamResponse.model_validate(team)

    async def delete(
        self, team_id: uuid.UUID, current_user: UserResponse
    ) -> None:
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipe não encontrada.",
            )
        # Garante que o usuário só deleta equipes da sua empresa
        check_same_company(current_user.company_id, team.company_id)
        await self.repo.delete(team)