from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    slug: Optional[str] = None

class ProjectInDB(ProjectBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class Project(ProjectInDB):
    pass 