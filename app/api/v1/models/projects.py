import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from ...db.database import Base


class ProjectStatus(enum.Enum):
    idea = "idea"
    in_progress = "in_progress"
    done = "done"


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    tags = Column(ARRAY(String))
    status = Column(Enum(ProjectStatus), default=ProjectStatus.idea, nullable=False)
    is_public = Column(Boolean, default=False)
    slug = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="projects")
    logs = relationship("Log", back_populates="project", cascade="all, delete-orphan")
