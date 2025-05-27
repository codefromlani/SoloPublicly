from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from ..schemas.logs import LogCreate, LogUpdate
from ..models.projects import Project
from ..models.logs import Log
from ..models.users import User

def create_log(project_id: UUID, log_data: LogCreate, db: Session, current_user: User) -> Log:
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or you don't have access"
        )
    
    existing_log = db.query(Log).filter(
        Log.project_id == project_id,
        Log.log_date == log_data.log_date
    ).first()

    if existing_log:
        existing_log.content_md = log_data.content_md
        db.commit()
        db.refresh(existing_log)
        return existing_log
    
    new_log = Log(
        project_id=project_id,
        content_md=log_data.content_md,
        log_date=log_data.log_date
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log

def get_project_logs(project_id: UUID, db: Session, current_user: User) -> List[Log]:
    project = db.query(Project).filter(
        project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or you don't have access"
        )
    
    logs = db.query(Log).filter(Log.project_id == project_id).order_by(Log.log_date.desc()).all()
    return logs

def get_log_by_id(log_id: UUID, db: Session, current_user: User) -> Log:
    log = db.query(Log).join(Project).filter(
        Log.id == log_id,
        Project.user_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found or you don't have access"
        )
    
    return log

def update_log(log_id: UUID, log_data: LogUpdate, db: Session, current_user: User) -> Log:
    log = get_log_by_id(log_id, db, current_user)

    update_data = log_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(log, field, value)

    db.commit()
    db.refresh(log)
    return log

def delete_log(log_id: UUID, db: Session, current_user: User):
    log = get_log_by_id(log_id, db, current_user)

    db.delete(log)
    db.commit()
    return {"message": "Log deleted successfully"}