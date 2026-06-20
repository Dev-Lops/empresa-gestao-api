from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Motor de conexão com o banco
# É criado uma vez e reutilizado durante toda a vida da aplicação
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)


# Fábrica de sessões
# Cada requisição recebe uma sessão própria criada por essa fábrica
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Classe base para todos os models
# Quando criarmos a tabela User, Company, etc — todas herdam daqui
class Base(DeclarativeBase):
    pass


# Dependency do FastAPI
# Cada endpoint que precisar do banco recebe uma sessão via Depends(get_db)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()