from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
import re
import unicodedata

from ..schemas.projects import ProjectCreate, ProjectUpdate
from ..models.projects import Project
from ..models.users import User


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)

def generate_unique_slug(title: str, db: Session) -> str:
    base_slug = slugify(title)
    slug = base_slug
    index = 1

    while db.query(Project).filter_by(slug=slug).first():
        slug = f"{base_slug}-index"
        index += 1

    return slug

def create_project_idea(project: ProjectCreate, db: Session, current_user: User) -> Project:
    project_data = project.dict(exclude_unset=True)
    project_data["slug"] = generate_unique_slug(project_data["title"], db)
    project_data["user_id"] = current_user.id

    new_project = Project(**project_data)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_project_by_ID(project_id: UUID, db: Session) -> Project:
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    return db_project

def get_project_by_slug(slug: str, db: Session) -> Project:
    db_project = db.query(Project).filter_by(slug=slug, is_public=True).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not public."
        )
    
    return db_project

def get_user_projects(db: Session, current_user: User, skip: int = 0, limit: int = 10) -> List[Project]:
    return db.query(Project).filter(Project.user_id == current_user.id).offset(skip).limit(limit).all()

def update_user_project(project_id: UUID, project_data: ProjectUpdate, db: Session, current_user: User) -> Optional[Project]:
    db_project = get_project_by_ID(project_id, db)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project

def delete_user_project(project_id: UUID, db: Session, current_user: User):
    db_project = get_project_by_ID(project_id, db)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}