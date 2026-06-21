import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import check_same_company
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.user import UserResponse


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProjectRepository(db)

    async def get_all(self, company_id: uuid.UUID) -> list[ProjectResponse]:
        projects = await self.repo.get_all(company_id)
        return [ProjectResponse.model_validate(p) for p in projects]

    async def get_by_id(self, project_id: uuid.UUID) -> ProjectResponse:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado.",
            )
        return ProjectResponse.model_validate(project)

    async def create(
        self, data: ProjectCreate, current_user: UserResponse
    ) -> ProjectResponse:
        check_same_company(current_user.company_id, data.company_id)
        project = await self.repo.create(data)
        return ProjectResponse.model_validate(project)

    async def update(
        self, project_id: uuid.UUID, data: ProjectUpdate, current_user: UserResponse
    ) -> ProjectResponse:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado.",
            )
        check_same_company(current_user.company_id, project.company_id)
        project = await self.repo.update(project, data)
        return ProjectResponse.model_validate(project)

    async def delete(
        self, project_id: uuid.UUID, current_user: UserResponse
    ) -> None:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado.",
            )
        check_same_company(current_user.company_id, project.company_id)
        await self.repo.delete(project)