"""Aplicação FastAPI — Customer Management Dashboard."""
import logging
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.core.exceptions import ClienteNaoEncontradoError, CpfDuplicadoError, EmailDuplicadoError
from app.routes import auth, clientes, dashboard, health

logger = logging.getLogger("customer_management_dashboard")
settings = get_settings()
app = FastAPI(title="Customer Management Dashboard API",
              description="API REST protegida para gestão administrativa de clientes.",
              version="1.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins_list,
                   allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                   allow_headers=["Content-Type"])

@app.exception_handler(ClienteNaoEncontradoError)
async def cliente_nao_encontrado_handler(request: Request, exc: ClienteNaoEncontradoError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

@app.exception_handler(EmailDuplicadoError)
async def email_duplicado_handler(request: Request, exc: EmailDuplicadoError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

@app.exception_handler(CpfDuplicadoError)
async def cpf_duplicado_handler(request: Request, exc: CpfDuplicadoError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

@app.exception_handler(Exception)
async def erro_inesperado_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Erro inesperado: method=%s path=%s exception_type=%s",
                 request.method, request.url.path, type(exc).__name__)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"detail": "erro interno do servidor"})

app.include_router(auth.router)
app.include_router(health.router)
app.include_router(clientes.router)
app.include_router(dashboard.router)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.is_dir():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/{caminho_completo:path}", include_in_schema=False)
    async def servir_frontend(caminho_completo: str) -> FileResponse:
        arquivo_estatico = FRONTEND_DIST / caminho_completo
        if caminho_completo and arquivo_estatico.is_file():
            return FileResponse(arquivo_estatico)
        return FileResponse(FRONTEND_DIST / "index.html")
