import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Company]:
        """Retorna todas as empresas."""
        result = await self.db.execute(select(Company))
        return list(result.scalars().all())

    async def get_by_id(self, company_id: uuid.UUID) -> Company | None:
        """Busca uma empresa pelo ID."""
        result = await self.db.execute(
            select(Company).where(Company.id == company_id)
        )
        return result.scalar_one_or_none()

    async def get_by_document(self, document: str) -> Company | None:
        """Busca uma empresa pelo CNPJ/documento."""
        result = await self.db.execute(
            select(Company).where(Company.document == document)
        )
        return result.scalar_one_or_none()

    async def create(self, data: CompanyCreate) -> Company:
        """Cria uma nova empresa."""
        company = Company(**data.model_dump())
        self.db.add(company)
        await self.db.flush()
        await self.db.refresh(company)
        return company

    async def update(self, company: Company, data: CompanyUpdate) -> Company:
        """
        Atualiza só os campos enviados.
        exclude_unset=True ignora campos não enviados pelo cliente.
        """
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(company, field, value)
        await self.db.flush()
        await self.db.refresh(company)
        return company

    async def delete(self, company: Company) -> None:
        """Remove uma empresa do banco."""
        await self.db.delete(company)
        await self.db.flush()