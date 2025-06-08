from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ....models.translation import TranslationKey, TranslationKeyCreate, TranslationKeyUpdate
from ....services.translation_service import TranslationService

router = APIRouter()

def get_translation_service() -> TranslationService:
    return TranslationService()

@router.post("/", response_model=TranslationKey)
async def create_translation(
    translation: TranslationKeyCreate,
    service: TranslationService = Depends(get_translation_service)
):
    return await service.create(translation)

@router.get("/project/{project_id}", response_model=List[TranslationKey])
async def list_project_translations(
    project_id: str,
    service: TranslationService = Depends(get_translation_service)
):
    return await service.list_by_project(project_id)

@router.get("/{translation_id}", response_model=TranslationKey)
async def get_translation(
    translation_id: str,
    service: TranslationService = Depends(get_translation_service)
):
    translation = await service.get(translation_id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@router.put("/{translation_id}", response_model=TranslationKey)
async def update_translation(
    translation_id: str,
    translation: TranslationKeyUpdate,
    service: TranslationService = Depends(get_translation_service)
):
    updated_translation = await service.update(translation_id, translation)
    if not updated_translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return updated_translation

@router.delete("/{translation_id}")
async def delete_translation(
    translation_id: str,
    service: TranslationService = Depends(get_translation_service)
):
    success = await service.delete(translation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Translation not found")
    return {"message": "Translation deleted successfully"}

@router.post("/bulk", response_model=List[TranslationKey])
async def bulk_update_translations(
    translations: List[TranslationKeyCreate],
    service: TranslationService = Depends(get_translation_service)
):
    return await service.bulk_update(translations) 