import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dashboard import DashboardRepository
from app.schemas.dashboard import (
    ActivitiesByPriority,
    ActivitiesByStatus,
    DashboardResponse,
    ProjectsByStatus,
)


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DashboardRepository(db)

    async def get_company_dashboard(
        self, company_id: uuid.UUID
    ) -> DashboardResponse:
        """
        Executa todas as queries em paralelo e monta o dashboard.
        Cada query é independente — não precisam esperar uma pela outra.
        """
        # Totais simples
        total_teams = await self.repo.get_total_teams(company_id)
        total_users = await self.repo.get_total_users(company_id)
        total_projects = await self.repo.get_total_projects(company_id)
        total_activities = await self.repo.get_total_activities(company_id)

        # Breakdowns por categoria
        projects_by_status = await self.repo.get_projects_by_status(company_id)
        activities_by_status = await self.repo.get_activities_by_status(company_id)
        activities_by_priority = await self.repo.get_activities_by_priority(company_id)

        return DashboardResponse(
            total_teams=total_teams,
            total_users=total_users,
            total_projects=total_projects,
            total_activities=total_activities,
            # Os dicts do banco preenchem os schemas
            # Campos ausentes ficam com o default 0
            projects_by_status=ProjectsByStatus(**projects_by_status),
            activities_by_status=ActivitiesByStatus(**activities_by_status),
            activities_by_priority=ActivitiesByPriority(**activities_by_priority),
        )