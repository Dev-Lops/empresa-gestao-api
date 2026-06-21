from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class ProjectStatus(enum.Enum):
    PLANNING = "planning"       # em planejamento
    IN_PROGRESS = "in_progress" # em andamento
    ON_HOLD = "on_hold"         # pausado
    COMPLETED = "completed"     # concluído
    CANCELLED = "cancelled"     # cancelado


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus),
        default=ProjectStatus.PLANNING,
        nullable=False,
    )

    # Chaves estrangeiras
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )
    team_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relacionamentos
    company: Mapped[Company] = relationship(back_populates="projects")
    team: Mapped[Team | None] = relationship(back_populates="projects")
    activities: Mapped[list[Activity]] = relationship(back_populates="project")