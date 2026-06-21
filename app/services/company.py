import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CompanyRepository(db)

    async def get_all(self) -> list[CompanyResponse]:
        companies = await self.repo.get_all()
        return [CompanyResponse.model_validate(c) for c in companies]

    async def get_by_id(self, company_id: uuid.UUID) -> CompanyResponse:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada.",
            )
        return CompanyResponse.model_validate(company)

    async def create(self, data: CompanyCreate) -> CompanyResponse:
        # Documento deve ser único
        existing = await self.repo.get_by_document(data.document)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Documento já cadastrado.",
            )
        company = await self.repo.create(data)
        return CompanyResponse.model_validate(company)

    async def update(
        self, company_id: uuid.UUID, data: CompanyUpdate
    ) -> CompanyResponse:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada.",
            )
        company = await self.repo.update(company, data)
        return CompanyResponse.model_validate(company)

    async def delete(self, company_id: uuid.UUID) -> None:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada.",
            )
        await self.repo.delete(company)