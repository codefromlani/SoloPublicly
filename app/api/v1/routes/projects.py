from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.projects import ProjectOut, ProjectCreate, ProjectUpdate, ProjectPublic
from ...db.database import get_db
from ..models.users import User
from ...core.security import get_current_user
from ..services.projects import create_project_idea, get_project_by_ID, get_project_by_slug, get_user_projects, update_user_project, delete_user_project


router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/create", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_project_idea(project, db, current_user)

@router.get("/get/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_project_by_ID(project_id, db)

@router.get("/public/{slug}", response_model=ProjectPublic)
def get_public_project(
    slug: str, 
    db: Session = Depends(get_db)
):
    return get_project_by_slug(slug, db)

@router.get("/all", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0, 
    limit: int = 10
):
    projects = get_user_projects(db, current_user, skip, limit)
    print("Retrieved projects:", projects)
    return projects

@router.patch("/update/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: UUID, 
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_user_project(project_id, project_data, db, current_user)
    
@router.delete("/delete/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_user_project(project_id, db, current_user)

