from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ....models.language import Language, LanguageCreate, LanguageUpdate
from ....services.language_service import LanguageService

router = APIRouter()

def get_language_service() -> LanguageService:
    return LanguageService()

@router.post("/", response_model=Language)
async def create_language(
    language: LanguageCreate,
    service: LanguageService = Depends(get_language_service)
):
    return await service.create(language)

@router.get("/", response_model=List[Language])
async def list_languages(
    service: LanguageService = Depends(get_language_service)
):
    return await service.list()

@router.get("/{code}", response_model=Language)
async def get_language(
    code: str,
    service: LanguageService = Depends(get_language_service)
):
    language = await service.get(code)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language

@router.put("/{code}", response_model=Language)
async def update_language(
    code: str,
    language: LanguageUpdate,
    service: LanguageService = Depends(get_language_service)
):
    updated_language = await service.update(code, language)
    if not updated_language:
        raise HTTPException(status_code=404, detail="Language not found")
    return updated_language

@router.delete("/{code}")
async def delete_language(
    code: str,
    service: LanguageService = Depends(get_language_service)
):
    success = await service.delete(code)
    if not success:
        raise HTTPException(status_code=404, detail="Language not found")
    return {"message": "Language deleted successfully"} 