from pydantic import BaseModel


class ProjectsByStatus(BaseModel):
    planning: int = 0
    in_progress: int = 0
    on_hold: int = 0
    completed: int = 0
    cancelled: int = 0


class ActivitiesByStatus(BaseModel):
    todo: int = 0
    in_progress: int = 0
    in_review: int = 0
    done: int = 0


class ActivitiesByPriority(BaseModel):
    low: int = 0
    medium: int = 0
    high: int = 0
    critical: int = 0


class DashboardResponse(BaseModel):
    # Totais gerais
    total_teams: int
    total_projects: int
    total_activities: int
    total_users: int

    # Breakdown por categoria
    projects_by_status: ProjectsByStatus
    activities_by_status: ActivitiesByStatus
    activities_by_priority: ActivitiesByPriority