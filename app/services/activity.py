import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import check_same_company
from app.models.user import UserRole
from app.repositories.activity import ActivityRepository
from app.repositories.project import ProjectRepository
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.schemas.user import UserResponse


class ActivityService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ActivityRepository(db)
        self.project_repo = ProjectRepository(db)

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

    async def create(
        self, data: ActivityCreate, current_user: UserResponse
    ) -> ActivityResponse:
        # Verifica se o projeto existe e pertence à empresa do usuário
        project = await self.project_repo.get_by_id(data.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado.",
            )
        check_same_company(current_user.company_id, project.company_id)
        activity = await self.repo.create(data)
        return ActivityResponse.model_validate(activity)

    async def update(
        self, activity_id: uuid.UUID, data: ActivityUpdate, current_user: UserResponse
    ) -> ActivityResponse:
        activity = await self.repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atividade não encontrada.",
            )

        # Regra especial para MEMBER:
        # só pode atualizar atividades atribuídas a ele mesmo
        if current_user.role == UserRole.MEMBER:
            if activity.responsible_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Você só pode atualizar atividades atribuídas a você.",
                )

        activity = await self.repo.update(activity, data)
        return ActivityResponse.model_validate(activity)

    async def delete(
        self, activity_id: uuid.UUID, current_user: UserResponse
    ) -> None:
        activity = await self.repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atividade não encontrada.",
            )
        project = await self.project_repo.get_by_id(activity.project_id)
        check_same_company(current_user.company_id, project.company_id)
        await self.repo.delete(activity)