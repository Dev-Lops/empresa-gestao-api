from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user import UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Cria uma nova conta e retorna o token de acesso."""
    service = AuthService(db)
    return await service.register(data)


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Autentica o usuário e retorna o token de acesso."""
    service = AuthService(db)
    return await service.login(data)


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: UserResponse = Depends(get_current_user),
):
    """Retorna os dados do usuário autenticado."""
    return current_user