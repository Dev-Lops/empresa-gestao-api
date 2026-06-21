import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user import UserRepository
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user import UserResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> AuthResponse:
        """
        Registra um novo usuário.
        Valida se email já existe, faz hash da senha e cria o usuário.
        """
        # Regra de negócio: email único
        if await self.user_repo.email_exists(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já cadastrado.",
            )

        # Nunca salvar senha em texto puro
        user = await self.user_repo.create({
            "name": data.name,
            "email": data.email,
            "hashed_password": hash_password(data.password),
            "company_id": uuid.UUID(data.company_id),
        })

        token = create_access_token(subject=user.email)

        return AuthResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    async def login(self, data: LoginRequest) -> AuthResponse:
        """
        Autentica um usuário.
        Valida email e senha, retorna token JWT se correto.
        """
        user = await self.user_repo.get_by_email(data.email)

        # Mesma mensagem para email não encontrado e senha errada
        # Motivo: não revelar se o email existe no sistema
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo.",
            )

        token = create_access_token(subject=user.email)

        return AuthResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    async def get_current_user_by_token(self, token: str) -> UserResponse:
        """
        Valida o token JWT e retorna o usuário correspondente.
        Usado pelo middleware de autenticação.
        """
        from app.core.security import decode_access_token

        email = decode_access_token(token)

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await self.user_repo.get_by_email(email)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado ou inativo.",
            )

        return UserResponse.model_validate(user)