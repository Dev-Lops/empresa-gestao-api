import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, require_manager
from app.core.database import get_db
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from app.schemas.user import UserResponse
from app.services.team import TeamService

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[TeamResponse])
async def list_teams(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Qualquer usuário autenticado pode listar equipes."""
    service = TeamService(db)
    return await service.get_all(company_id)


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = TeamService(db)
    return await service.get_by_id(team_id)


@router.post("/", response_model=TeamResponse, status_code=201)
async def create_team(
    data: TeamCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_manager),
):
    """ADMIN e MANAGER podem criar equipes."""
    service = TeamService(db)
    return await service.create(data, current_user)


@router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: uuid.UUID,
    data: TeamUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_manager),
):
    """ADMIN e MANAGER podem atualizar equipes."""
    service = TeamService(db)
    return await service.update(team_id, data, current_user)


@router.delete("/{team_id}", status_code=204)
async def delete_team(
    team_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_manager),
):
    """ADMIN e MANAGER podem deletar equipes."""
    service = TeamService(db)
    await service.delete(team_id, current_user)