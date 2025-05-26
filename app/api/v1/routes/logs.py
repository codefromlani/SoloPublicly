from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from ..schemas.logs import LogCreate, LogUpdate, LogOut
from ...db.database import get_db
from ..models.users import User
from ...core.security import get_current_user
from ..services.logs import create_log, get_project_logs, get_log_by_id, update_log, delete_log

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post("/project/{project_id}", response_model=LogOut, status_code=status.HTTP_201_CREATED)
def create_project_log(
    project_id: UUID,
    log_data: LogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_log(project_id, log_data, db, current_user)

@router.get("/project/{project_id}", response_model=List[LogOut])
def get_logs_for_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_project_logs(project_id, db, current_user)

@router.get("/{log_id}", response_model=LogOut)
def get_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_log_by_id(log_id, db, current_user)

@router.patch("/{log_id}", response_model=LogOut)
def update_project_log(
    log_id: UUID,
    log_data: LogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_log(log_id, log_data, db, current_user)

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_log(log_id, db, current_user)