from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserResponse
from app.services.auth import AuthService

# Diz ao FastAPI onde fica o endpoint de login
# Isso habilita o botão "Authorize" no Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Dependency reutilizável para rotas protegidas.

    Uso nos endpoints:
        @router.get("/me")
        async def me(user: UserResponse = Depends(get_current_user)):
            return user
    """
    service = AuthService(db)
    return await service.get_current_user_by_token(token)