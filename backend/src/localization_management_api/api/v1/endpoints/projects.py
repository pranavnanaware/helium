from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ....models.project import Project, ProjectCreate, ProjectUpdate
from ....services.project_service import ProjectService

router = APIRouter()

def get_project_service() -> ProjectService:
    return ProjectService()

@router.post("/", response_model=Project)
async def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    return await service.create(project)

@router.get("/", response_model=List[Project])
async def list_projects(
    service: ProjectService = Depends(get_project_service)
):
    return await service.list()

@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service)
):
    project = await service.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    updated_project = await service.update(project_id, project)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service)
):
    success = await service.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"} 