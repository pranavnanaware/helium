from typing import List, Optional, Dict
from datetime import datetime
from ..db.supabase import get_supabase_client
from ..models.translation import TranslationKeyCreate, TranslationKeyUpdate, TranslationKey, TranslationValue

class TranslationService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.keys_table = "translation_keys"
        self.translations_table = "translations"

    async def create(self, translation: TranslationKeyCreate) -> TranslationKey:
        # Create translation key
        key_response = self.supabase.table(self.keys_table) \
            .insert({
                "project_id": translation.project_id,
                "key": translation.key,
                "category": translation.category,
                "description": translation.description
            }) \
            .execute()
        
        key_id = key_response.data[0]["id"]
        
        # Create translations
        translations = []
        for lang_code, value in translation.translations.items():
            translation_response = self.supabase.table(self.translations_table) \
                .insert({
                    "translation_key_id": key_id,
                    "language_code": lang_code,
                    "value": value.value,
                    "updated_by": value.updated_by
                }) \
                .execute()
            translations.append(translation_response.data[0])
        
        return TranslationKey(
            **key_response.data[0],
            translations={lang_code: TranslationValue(**value) for lang_code, value in translation.translations.items()}
        )

    async def get(self, translation_id: str) -> Optional[TranslationKey]:
        # Get translation key
        key_response = self.supabase.table(self.keys_table) \
            .select("*") \
            .eq("id", translation_id) \
            .execute()
        
        if not key_response.data:
            return None
        
        # Get translations
        translations_response = self.supabase.table(self.translations_table) \
            .select("*") \
            .eq("translation_key_id", translation_id) \
            .execute()
        
        translations = {
            item["language_code"]: TranslationValue(
                value=item["value"],
                updated_at=item["updated_at"],
                updated_by=item["updated_by"]
            )
            for item in translations_response.data
        }
        
        return TranslationKey(
            **key_response.data[0],
            translations=translations
        )

    async def list_by_project(self, project_id: str) -> List[TranslationKey]:
        # Get all translation keys for project
        keys_response = self.supabase.table(self.keys_table) \
            .select("*") \
            .eq("project_id", project_id) \
            .execute()
        
        result = []
        for key in keys_response.data:
            # Get translations for each key
            translations_response = self.supabase.table(self.translations_table) \
                .select("*") \
                .eq("translation_key_id", key["id"]) \
                .execute()
            
            translations = {
                item["language_code"]: TranslationValue(
                    value=item["value"],
                    updated_at=item["updated_at"],
                    updated_by=item["updated_by"]
                )
                for item in translations_response.data
            }
            
            result.append(TranslationKey(
                **key,
                translations=translations
            ))
        
        return result

    async def update(self, translation_id: str, translation: TranslationKeyUpdate) -> Optional[TranslationKey]:
        # Update translation key
        key_data = translation.dict(exclude_unset=True, exclude={"translations"})
        if key_data:
            key_response = self.supabase.table(self.keys_table) \
                .update(key_data) \
                .eq("id", translation_id) \
                .execute()
            
            if not key_response.data:
                return None
        
        # Update translations if provided
        if translation.translations:
            for lang_code, value in translation.translations.items():
                self.supabase.table(self.translations_table) \
                    .upsert({
                        "translation_key_id": translation_id,
                        "language_code": lang_code,
                        "value": value.value,
                        "updated_by": value.updated_by
                    }) \
                    .execute()
        
        return await self.get(translation_id)

    async def delete(self, translation_id: str) -> bool:
        response = self.supabase.table(self.keys_table) \
            .delete() \
            .eq("id", translation_id) \
            .execute()
        return bool(response.data)

    async def bulk_update(self, translations: List[TranslationKeyCreate]) -> List[TranslationKey]:
        results = []
        for translation in translations:
            result = await self.create(translation)
            results.append(result)
        return results 