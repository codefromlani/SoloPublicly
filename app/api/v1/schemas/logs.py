from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class LogBase(BaseModel):
    content_md: str
    log_date: date = Field(default_factory=date.today)

class LogCreate(LogBase):
    pass

class LogUpdate(BaseModel):
    content_md: Optional[str] = None
    log_date: Optional[date] = None

class LogOut(LogBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True
    )