import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.schemas.user import UserResponse
from app.services.company import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=list[CompanyResponse])
async def list_companies(
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Lista todas as empresas."""
    service = CompanyService(db)
    return await service.get_all()


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Busca uma empresa pelo ID."""
    service = CompanyService(db)
    return await service.get_by_id(company_id)


@router.post("/", response_model=CompanyResponse, status_code=201)
async def create_company(
    data: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Cria uma nova empresa."""
    service = CompanyService(db)
    return await service.create(data)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: uuid.UUID,
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Atualiza parcialmente uma empresa."""
    service = CompanyService(db)
    return await service.update(company_id, data)


@router.delete("/{company_id}", status_code=204)
async def delete_company(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Remove uma empresa."""
    service = CompanyService(db)
    await service.delete(company_id)