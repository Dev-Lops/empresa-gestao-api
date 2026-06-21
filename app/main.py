from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.v1 import auth as auth_router
from app.api.v1 import companies as companies_router
from app.api.v1 import teams as teams_router
from app.api.v1 import projects as projects_router
from app.api.v1 import activities as activities_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tudo aqui roda quando a aplicação INICIA
    print(f"🚀 {settings.PROJECT_NAME} iniciando...")
    yield
    # Tudo aqui roda quando a aplicação ENCERRA
    print("👋 Encerrando aplicação")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="API REST para gestão de empresas, equipes, projetos e atividades.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_router.router,
    prefix=settings.API_V1_STR,
)

app.include_router(
    companies_router.router, 
    prefix=settings.API_V1_STR
)

app.include_router(
    teams_router.router, 
    prefix=settings.API_V1_STR
)

app.include_router(
    projects_router.router, 
    prefix=settings.API_V1_STR
)

app.include_router(
    activities_router.router, 
    prefix=settings.API_V1_STR
)


@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0",
    }