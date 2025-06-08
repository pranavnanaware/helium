from typing import List, Optional
from ..db.supabase import get_supabase_client
from ..models.project import ProjectCreate, ProjectUpdate, Project

class ProjectService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table = "projects"

    async def create(self, project: ProjectCreate) -> Project:
        response = self.supabase.table(self.table) \
            .insert(project.dict()) \
            .execute()
        return Project(**response.data[0])

    async def get(self, project_id: str) -> Optional[Project]:
        response = self.supabase.table(self.table) \
            .select("*") \
            .eq("id", project_id) \
            .execute()
        
        if not response.data:
            return None
        return Project(**response.data[0])

    async def list(self) -> List[Project]:
        response = self.supabase.table(self.table) \
            .select("*") \
            .execute()
        return [Project(**item) for item in response.data]

    async def update(self, project_id: str, project: ProjectUpdate) -> Optional[Project]:
        response = self.supabase.table(self.table) \
            .update(project.dict(exclude_unset=True)) \
            .eq("id", project_id) \
            .execute()
        
        if not response.data:
            return None
        return Project(**response.data[0])

    async def delete(self, project_id: str) -> bool:
        response = self.supabase.table(self.table) \
            .delete() \
            .eq("id", project_id) \
            .execute()
        return bool(response.data) 