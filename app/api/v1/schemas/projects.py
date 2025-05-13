from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class ProjectStatus(str, Enum):
    idea = "idea"
    in_progress = "in_progress"
    done = "done"


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: ProjectStatus = ProjectStatus.idea
    is_public: bool = False

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[ProjectStatus] = None
    is_public: Optional[bool] = None
    slug: Optional[str] = None

class ProjectOut(ProjectBase):
    id: UUID
    user_id: UUID
    slug: str
    created_at: datetime
    updated_at: datetime

class ProjectPublic(BaseModel):
    title: str
    description: Optional[str]
    tags: Optional[List[str]]
    status: ProjectStatus
    created_at: datetime
    slug: str

    model_config = ConfigDict(
        from_attributes=True
    )