import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app.utils.dependencies import get_db

SQLALCHEMY_TEST_URL = "sqlite://"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionTest = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db():
    session = SessionTest()
    try:
        yield session
    finally:
        session.close()


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
    client.post("/auth/signup", json=usuario_dados)
    resp = client.post("/auth/login", json={
        "email": usuario_dados["email"],
        "senha": usuario_dados["senha"],
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
