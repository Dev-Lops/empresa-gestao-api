from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import UserRole
from app.schemas.user import UserResponse
from app.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ─── Dependency base ──────────────────────────────────────────────────────────
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Valida o token e retorna o usuário logado."""
    service = AuthService(db)
    return await service.get_current_user_by_token(token)


# ─── Dependencies de papel ────────────────────────────────────────────────────
async def require_admin(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """Apenas ADMINs passam."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores.",
        )
    return current_user


async def require_manager(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """ADMINs e MANAGERs passam."""
    if current_user.role not in (UserRole.ADMIN, UserRole.MANAGER):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a gerentes e administradores.",
        )
    return current_user


# ─── Dependency de isolamento por empresa ─────────────────────────────────────
async def get_current_company_id(
    current_user: UserResponse = Depends(get_current_user),
) -> UUID:
    """
    Retorna o company_id do usuário logado.
    Usado para garantir que o usuário só acessa dados da sua empresa.
    """
    return current_user.company_id


def check_same_company(user_company_id: UUID, resource_company_id: UUID) -> None:
    """
    Verifica se o recurso pertence à empresa do usuário.
    Lança 403 se não pertencer.
    """
    if user_company_id != resource_company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Recurso pertence a outra empresa.",
        )