"""
Testes unitários para a API de Biblioteca Virtual.

Utiliza:
- pytest: framework de testes.
- TestClient (Starlette): cliente HTTP para simular requests à API.
- Banco SQLite em memória com StaticPool: isola os testes do banco de produção.

Estratégia:
- Usa StaticPool para que todas as conexões compartilhem o mesmo banco
  em memória (SQLite cria bancos separados por conexão por padrão).
- A dependency injection do FastAPI é sobrescrita (override) para usar
  o banco de testes ao invés do banco real.
- Cada teste recria as tabelas para garantir isolamento.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


# --- Configuração do banco de testes (SQLite em memória) ---
# StaticPool garante que todas as conexões usem a MESMA instância
# do banco em memória — sem isso, cada conexão teria um banco separado.
engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    """
    Substitui a dependency get_db nos testes.
    Usa o banco em memória ao invés do banco real.
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Sobrescreve a dependency no app do FastAPI
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """
    Fixture que roda antes de CADA teste:
    - Cria todas as tabelas no banco em memória (de teste).
    - Após o teste, remove todas as tabelas (limpeza).

    autouse=True faz com que essa fixture seja aplicada
    automaticamente em todos os testes do módulo.
    """
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


# Client de testes — simula requests HTTP sem iniciar o servidor
client = TestClient(app, raise_server_exceptions=True)


# --- Testes ---

def test_criar_livro():
    """Testa a criação de um livro via POST /livros/."""
    payload = {
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "data_publicacao": "2008-08-01",
        "resumo": "Guia sobre boas práticas de programação."
    }

    response = client.post("/livros/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Clean Code"
    assert data["autor"] == "Robert C. Martin"
    assert "id" in data  # Verifica que o id foi gerado


def test_listar_livros():
    """Testa a listagem de todos os livros via GET /livros/."""
    client.post("/livros/", json={
        "titulo": "Livro A",
        "autor": "Autor A",
        "data_publicacao": "2020-01-01",
        "resumo": "Resumo A"
    })
    client.post("/livros/", json={
        "titulo": "Livro B",
        "autor": "Autor B",
        "data_publicacao": "2021-01-01",
        "resumo": "Resumo B"
    })

    response = client.get("/livros/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_buscar_por_titulo():
    """Testa a busca de livros por título via GET /livros/busca/?titulo=..."""
    client.post("/livros/", json={
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "data_publicacao": "1899-01-01",
        "resumo": "Clássico da literatura brasileira."
    })
    client.post("/livros/", json={
        "titulo": "O Cortiço",
        "autor": "Aluísio Azevedo",
        "data_publicacao": "1890-01-01",
        "resumo": "Romance naturalista."
    })

    # Busca parcial e case-insensitive
    response = client.get("/livros/busca/?titulo=dom")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["titulo"] == "Dom Casmurro"


def test_buscar_por_autor():
    """Testa a busca de livros por autor via GET /livros/busca/?autor=..."""
    client.post("/livros/", json={
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "data_publicacao": "1899-01-01",
        "resumo": "Clássico."
    })
    client.post("/livros/", json={
        "titulo": "Memórias Póstumas de Brás Cubas",
        "autor": "Machado de Assis",
        "data_publicacao": "1881-01-01",
        "resumo": "Outro clássico."
    })
    client.post("/livros/", json={
        "titulo": "O Cortiço",
        "autor": "Aluísio Azevedo",
        "data_publicacao": "1890-01-01",
        "resumo": "Naturalismo."
    })

    response = client.get("/livros/busca/?autor=machado")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Dois livros do Machado


def test_buscar_sem_resultado():
    """Testa que busca sem resultado retorna lista vazia."""
    response = client.get("/livros/busca/?titulo=livro_inexistente_xyz")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
