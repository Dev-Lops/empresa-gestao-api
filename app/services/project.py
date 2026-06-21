import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate


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

    async def create(self, data: ProjectCreate) -> ProjectResponse:
        project = await self.repo.create(data)
        return ProjectResponse.model_validate(project)

    async def update(self, project_id: uuid.UUID, data: ProjectUpdate) -> ProjectResponse:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado.",
            )
        project = await self.repo.update(project, data)
        return ProjectResponse.model_validate(project)

    async def delete(self, project_id: uuid.UUID) -> None:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado.",
            )
        await self.repo.delete(project)