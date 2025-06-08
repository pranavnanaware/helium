from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .api.v1.endpoints import projects, languages, translations

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    projects.router,
    prefix=f"{settings.API_V1_STR}/projects",
    tags=["projects"]
)

app.include_router(
    languages.router,
    prefix=f"{settings.API_V1_STR}/languages",
    tags=["languages"]
)

app.include_router(
    translations.router,
    prefix=f"{settings.API_V1_STR}/translations",
    tags=["translations"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Localization Management API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }


