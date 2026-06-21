import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class CompanyCreate(BaseModel):
    """Dados para criar uma empresa."""
    name: str
    document: str
    email: EmailStr
    phone: str | None = None
    description: str | None = None


class CompanyUpdate(BaseModel):
    """
    Dados para atualizar uma empresa.
    Todos os campos são opcionais — só atualiza o que for enviado.
    """
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    description: str | None = None
    is_active: bool | None = None


class CompanyResponse(BaseModel):
    """Dados retornados pela API."""
    id: uuid.UUID
    name: str
    document: str
    email: str
    phone: str | None
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}