from pydantic import BaseModel
from typing import Optional

class LanguageBase(BaseModel):
    code: str
    name: str

class LanguageCreate(LanguageBase):
    pass

class LanguageUpdate(LanguageBase):
    code: Optional[str] = None
    name: Optional[str] = None

class Language(LanguageBase):
    class Config:
        from_attributes = True 