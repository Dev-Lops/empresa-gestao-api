import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        # Recebe a sessão do banco como dependência
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        """Busca um usuário pelo email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Busca um usuário pelo ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: dict) -> User:
        """Cria um novo usuário no banco."""
        user = User(**user_data)
        self.db.add(user)
        await self.db.flush()   # envia ao banco mas não commita ainda
        await self.db.refresh(user)  # recarrega o objeto com dados do banco
        return user

    async def email_exists(self, email: str) -> bool:
        """Verifica se um email já está cadastrado."""
        user = await self.get_by_email(email)
        return user is not None