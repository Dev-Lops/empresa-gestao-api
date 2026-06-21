import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity, ActivityPriority, ActivityStatus
from app.models.project import Project, ProjectStatus
from app.models.team import Team
from app.models.user import User


class DashboardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_total_teams(self, company_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(Team.id)).where(Team.company_id == company_id)
        )
        return result.scalar() or 0

    async def get_total_users(self, company_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(User.id)).where(User.company_id == company_id)
        )
        return result.scalar() or 0

    async def get_total_projects(self, company_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(Project.id)).where(Project.company_id == company_id)
        )
        return result.scalar() or 0

    async def get_total_activities(self, company_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(Activity.id))
            .join(Project, Activity.project_id == Project.id)
            .where(Project.company_id == company_id)
        )
        return result.scalar() or 0

    async def get_projects_by_status(self, company_id: uuid.UUID) -> dict:
        """
        Retorna contagem de projetos agrupados por status.
        O banco faz o agrupamento — muito mais eficiente que buscar tudo e contar no Python.
        """
        result = await self.db.execute(
            select(Project.status, func.count(Project.id))
            .where(Project.company_id == company_id)
            .group_by(Project.status)
        )
        # Converte lista de tuplas em dicionário
        # [("planning", 3), ("in_progress", 2)] → {"planning": 3, "in_progress": 2}
        return {row[0].value: row[1] for row in result.all()}

    async def get_activities_by_status(self, company_id: uuid.UUID) -> dict:
        result = await self.db.execute(
            select(Activity.status, func.count(Activity.id))
            .join(Project, Activity.project_id == Project.id)
            .where(Project.company_id == company_id)
            .group_by(Activity.status)
        )
        return {row[0].value: row[1] for row in result.all()}

    async def get_activities_by_priority(self, company_id: uuid.UUID) -> dict:
        result = await self.db.execute(
            select(Activity.priority, func.count(Activity.id))
            .join(Project, Activity.project_id == Project.id)
            .where(Project.company_id == company_id)
            .group_by(Activity.priority)
        )
        return {row[0].value: row[1] for row in result.all()}