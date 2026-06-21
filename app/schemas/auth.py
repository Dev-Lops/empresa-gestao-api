from pydantic import BaseModel, EmailStr

from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    """Dados enviados pelo usuário para fazer login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token retornado após login bem-sucedido."""
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    """Dados para criar conta e já retornar o token."""
    name: str
    email: EmailStr
    password: str
    company_id: str      # receberemos como string e converteremos


class AuthResponse(BaseModel):
    """Resposta completa do registro/login."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse