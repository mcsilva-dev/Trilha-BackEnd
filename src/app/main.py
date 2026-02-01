from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="SGHSS - Sistemas de Gestão de Hospitalar",
    description="API para gerenciamento de hospitalar",
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


@app.get("/", tags=["Root"])
def root():
    return {"message": "Bem-vindo ao Sistemas de Gestão de Hospitalar"}