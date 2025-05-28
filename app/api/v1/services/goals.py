from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from datetime import date, timedelta

from ..schemas.goals import WeeklyGoalCreate
from ..models.projects import Project
from ..models.goals import WeeklyGoal
from ..models.users import User

def create_or_update_weekly_goal(goal_data: WeeklyGoalCreate, db: Session, current_user: User) -> WeeklyGoal:
    start_of_week = goal_data.week_start_date

    existing_goal = db.query(WeeklyGoal).filter(
        WeeklyGoal.user_id == current_user.id,
        WeeklyGoal.week_start_date == start_of_week
    ).first()

    if existing_goal:
        existing_goal.goal_text = goal_data.goal_text
        db.commit()
        db.refresh(existing_goal)
        return existing_goal
    
    new_goal = WeeklyGoal(
        user_id=current_user.id,
        week_start_date=start_of_week,
        goal_text=goal_data.goal_text
    )
    
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    
    return new_goal

def get_current_weekly_goal(db: Session, current_user: User) -> Optional[WeeklyGoal]:
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    goal = db.query(WeeklyGoal).filter(
        WeeklyGoal.user_id == current_user.id,
        WeeklyGoal.week_start_date == start_of_week
    ).first()

    return 

def get_user_weekly_goals(db: Session, current_user: User) -> List[WeeklyGoal]:
    goals = db.query(WeeklyGoal).filter(
        WeeklyGoal.user_id == current_user.id
    ).order_by(WeeklyGoal.week_start_date.desc()).all()
    
    return goals

def delete_weekly_goal(goal_id: UUID, db: Session, current_user: User):
    goal = db.query(WeeklyGoal).filter(
        WeeklyGoal.id == goal_id,
        WeeklyGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found or you don't have access"
        )
    
    db.delete(goal)
    db.commit()
    return {"message": "Weekly goal deleted successfully"}