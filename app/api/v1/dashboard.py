import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.schemas.dashboard import DashboardResponse
from app.schemas.user import UserResponse
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/company/{company_id}", response_model=DashboardResponse)
async def get_company_dashboard(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retorna métricas consolidadas de uma empresa.
    Qualquer usuário autenticado pode visualizar o dashboard.
    """
    service = DashboardService(db)
    return await service.get_company_dashboard(company_id)