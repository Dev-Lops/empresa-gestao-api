from __future__ import annotations

import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class UserRole(enum.Enum):
    ADMIN = "admin"       # acesso total à empresa
    MANAGER = "manager"   # gerencia equipes e projetos
    MEMBER = "member"     # acesso básico


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.MEMBER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Chave estrangeira — liga o usuário à empresa
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relacionamentos
    company: Mapped[Company] = relationship(back_populates="users")
    teams: Mapped[list[Team]] = relationship(
        secondary="team_members",
        back_populates="members",
    )
    activities: Mapped[list[Activity]] = relationship(back_populates="responsible")