from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class ActivityStatus(enum.Enum):
    TODO = "todo"           # a fazer
    IN_PROGRESS = "in_progress" # em andamento
    IN_REVIEW = "in_review"     # em revisão
    DONE = "done"               # concluída


class ActivityPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Activity(Base, TimestampMixin):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ActivityStatus] = mapped_column(
        Enum(ActivityStatus),
        default=ActivityStatus.TODO,
        nullable=False,
    )
    priority: Mapped[ActivityPriority] = mapped_column(
        Enum(ActivityPriority),
        default=ActivityPriority.MEDIUM,
        nullable=False,
    )

    # Chaves estrangeiras
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    responsible_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relacionamentos
    project: Mapped[Project] = relationship(back_populates="activities")
    responsible: Mapped[User | None] = relationship(back_populates="activities")