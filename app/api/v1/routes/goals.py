from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from ..schemas.goals import WeeklyGoalCreate, WeeklyGoalOut
from ...db.database import get_db
from ..models.users import User
from ...core.security import get_current_user
from ..services.goals import create_or_update_weekly_goal, get_current_weekly_goal, get_user_weekly_goals, delete_weekly_goal

router = APIRouter(prefix="/weekly-goals", tags=["goals"])

@router.post("/", response_model=WeeklyGoalOut, status_code=status.HTTP_201_CREATED)
def create_weekly_goal(
    goal_data: WeeklyGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_or_update_weekly_goal(goal_data, db, current_user)

@router.get("/current", response_model=Optional[WeeklyGoalOut])
def get_current_goal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_current_weekly_goal(db, current_user)

@router.get("/all", response_model=List[WeeklyGoalOut])
def get_all_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_weekly_goals(db, current_user)

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_weekly_goal(goal_id, db, current_user)