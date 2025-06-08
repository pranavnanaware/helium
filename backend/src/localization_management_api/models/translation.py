from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class TranslationValue(BaseModel):
    value: str
    updated_at: datetime
    updated_by: str

class TranslationKeyBase(BaseModel):
    key: str
    category: Optional[str] = None
    description: Optional[str] = None
    project_id: str

class TranslationKeyCreate(TranslationKeyBase):
    translations: Dict[str, TranslationValue]

class TranslationKeyUpdate(TranslationKeyBase):
    key: Optional[str] = None
    translations: Optional[Dict[str, TranslationValue]] = None

class TranslationKeyInDB(TranslationKeyBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class TranslationKey(TranslationKeyInDB):
    translations: Dict[str, TranslationValue] 