from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class WeeklyGoalBase(BaseModel):
    goal_text: str
    week_start_date: date

class WeeklyGoalCreate(WeeklyGoalBase):
    pass

class WeeklyGoalUpdate(BaseModel):
    goal_text: Optional[str] = None

class WeeklyGoalOut(WeeklyGoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True
    )