import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    """Dados necessários para criar um usuário."""
    name: str
    email: EmailStr      # valida formato de email automaticamente
    password: str
    company_id: uuid.UUID


class UserResponse(BaseModel):
    """Dados retornados pela API — nunca incluímos a senha."""
    id: uuid.UUID
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    company_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}  # permite ler de objetos ORM