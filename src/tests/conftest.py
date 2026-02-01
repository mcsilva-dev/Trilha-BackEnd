import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app.utils.dependencies import get_db

SQLALCHAMY_TEST_URL = "sqlite://"

engine = create_engine(
    SQLALCHAMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

session_test = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = session_test()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def usuario_dados():
    return {
        "nome": "João Silva",
        "email": "joao@email.com",
        "senha": "senha123",
        "tipo_usuario": "paciente",
    }


@pytest.fixture
def auth_header(client, usuario_dados):
    client.post("/auth/singup", json=usuario_dados)
    response = client.post("/auth/login", json={"email": usuario_dados["email"], "senha": usuario_dados["senha"]})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
