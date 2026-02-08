from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, pacientes, medicos, consultas, prontuarios

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
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"},
    )


app.include_router(auth.router)
app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(consultas.router)
app.include_router(prontuarios.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Bem-vindo ao Sistemas de Gestão de Hospitalar"}