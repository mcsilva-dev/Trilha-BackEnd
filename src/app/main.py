import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, pacientes, medicos, consultas, prontuarios, prescricoes, exames

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("sghss")

app = FastAPI(
    title="SGHSS - Sistema de Gestão Hospitalar",
    description="API do Sistema de Gestão Hospitalar e de Serviços de Saúde da VidaPlus",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def handler_erro_geral(request: Request, exc: Exception):
    logger.error("Erro não tratado em %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"},
    )


@app.middleware("http")
async def middleware_log_requests(request: Request, call_next):
    logger.info(">> %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("<< %s %s [%s]", request.method, request.url.path, response.status_code)
    return response


app.include_router(auth.router)
app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(consultas.router)
app.include_router(prontuarios.router)
app.include_router(prescricoes.router)
app.include_router(exames.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Bem-vindo ao Sistemas de Gestão de Hospitalar"}