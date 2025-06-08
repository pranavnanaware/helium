import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from src.localization_management_api.main import app

client = TestClient(app)

# Project tests
def test_create_project():
    project_data = {
        "name": "Test Project",
        "slug": "test-project",
        "description": "A test project"
    }
    
    response = client.post("/projects", json=project_data)
    assert response.status_code == 200
    assert response.json()["name"] == project_data["name"]
    assert response.json()["slug"] == project_data["slug"]

def test_list_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_project():
    # First create a project
    project_data = {
        "name": "Test Project 2",
        "slug": "test-project-2",
        "description": "Another test project"
    }
    
    create_response = client.post("/projects", json=project_data)
    project_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] == project_data["name"]

# Language tests
def test_create_language():
    language_data = {
        "code": "en",
        "name": "English"
    }
    
    response = client.post("/languages", json=language_data)
    assert response.status_code == 200
    assert response.json()["code"] == language_data["code"]
    assert response.json()["name"] == language_data["name"]

def test_list_languages():
    response = client.get("/languages")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Translation tests
def test_get_localizations():
    response = client.get("/localizations/test-project/en")
    assert response.status_code == 404  # Since we don't have any data yet

def test_create_localization():
    # First create a project
    project_data = {
        "name": "Test Project 3",
        "slug": "test-project-3",
        "description": "Project for translations"
    }
    project_response = client.post("/projects", json=project_data)
    project_id = project_response.json()["id"]
    
    # Create a language
    language_data = {
        "code": "fr",
        "name": "French"
    }
    client.post("/languages", json=language_data)
    
    translation_data = {
        "project_id": project_id,
        "key": "button.save",
        "category": "buttons",
        "description": "Save button text",
        "translations": {
            "fr": {
                "value": "Enregistrer",
                "updated_at": datetime.now().isoformat(),
                "updated_by": "test-user"
            }
        }
    }
    
    response = client.post("/localizations", json=translation_data)
    assert response.status_code == 200
    assert response.json()["key"] == translation_data["key"]
    assert len(response.json()["translations"]) == 1

def test_update_localization():
    # First create a project
    project_data = {
        "name": "Test Project 4",
        "slug": "test-project-4",
        "description": "Project for updates"
    }
    project_response = client.post("/projects", json=project_data)
    project_id = project_response.json()["id"]
    
    # Create a language
    language_data = {
        "code": "es",
        "name": "Spanish"
    }
    client.post("/languages", json=language_data)
    
    # Create a translation
    translation_data = {
        "project_id": project_id,
        "key": "button.cancel",
        "category": "buttons",
        "description": "Cancel button text",
        "translations": {
            "es": {
                "value": "Cancelar",
                "updated_at": datetime.now().isoformat(),
                "updated_by": "test-user"
            }
        }
    }
    
    create_response = client.post("/localizations", json=translation_data)
    translation_id = create_response.json()["id"]
    
    # Update the translation
    updated_data = translation_data.copy()
    updated_data["translations"]["es"]["value"] = "Descartar"
    
    response = client.put(f"/localizations/{translation_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["translations"][0]["value"] == "Descartar"

def test_bulk_update_localizations():
    # First create a project
    project_data = {
        "name": "Test Project 5",
        "slug": "test-project-5",
        "description": "Project for bulk updates"
    }
    project_response = client.post("/projects", json=project_data)
    project_id = project_response.json()["id"]
    
    # Create languages
    languages = [
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"}
    ]
    for lang in languages:
        client.post("/languages", json=lang)
    
    translations = [
        {
            "project_id": project_id,
            "key": "button.save",
            "category": "buttons",
            "translations": {
                "de": {
                    "value": "Speichern",
                    "updated_at": datetime.now().isoformat(),
                    "updated_by": "test-user"
                }
            }
        },
        {
            "project_id": project_id,
            "key": "button.cancel",
            "category": "buttons",
            "translations": {
                "it": {
                    "value": "Annulla",
                    "updated_at": datetime.now().isoformat(),
                    "updated_by": "test-user"
                }
            }
        }
    ]
    
    response = client.post("/localizations/bulk", json=translations)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_delete_localization():
    # First create a project
    project_data = {
        "name": "Test Project 6",
        "slug": "test-project-6",
        "description": "Project for deletion"
    }
    project_response = client.post("/projects", json=project_data)
    project_id = project_response.json()["id"]
    
    # Create a language
    language_data = {
        "code": "pt",
        "name": "Portuguese"
    }
    client.post("/languages", json=language_data)
    
    # Create a translation
    translation_data = {
        "project_id": project_id,
        "key": "button.delete",
        "category": "buttons",
        "translations": {
            "pt": {
                "value": "Excluir",
                "updated_at": datetime.now().isoformat(),
                "updated_by": "test-user"
            }
        }
    }
    
    create_response = client.post("/localizations", json=translation_data)
    translation_id = create_response.json()["id"]
    
    # Delete the translation
    response = client.delete(f"/localizations/{translation_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/localizations/{translation_id}")
    assert get_response.status_code == 404 