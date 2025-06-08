from typing import List, Optional
from ..db.supabase import get_supabase_client
from ..models.language import LanguageCreate, LanguageUpdate, Language

class LanguageService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table = "languages"

    async def create(self, language: LanguageCreate) -> Language:
        response = self.supabase.table(self.table) \
            .insert(language.dict()) \
            .execute()
        return Language(**response.data[0])

    async def get(self, code: str) -> Optional[Language]:
        response = self.supabase.table(self.table) \
            .select("*") \
            .eq("code", code) \
            .execute()
        
        if not response.data:
            return None
        return Language(**response.data[0])

    async def list(self) -> List[Language]:
        response = self.supabase.table(self.table) \
            .select("*") \
            .execute()
        return [Language(**item) for item in response.data]

    async def update(self, code: str, language: LanguageUpdate) -> Optional[Language]:
        response = self.supabase.table(self.table) \
            .update(language.dict(exclude_unset=True)) \
            .eq("code", code) \
            .execute()
        
        if not response.data:
            return None
        return Language(**response.data[0])

    async def delete(self, code: str) -> bool:
        response = self.supabase.table(self.table) \
            .delete() \
            .eq("code", code) \
            .execute()
        return bool(response.data) 