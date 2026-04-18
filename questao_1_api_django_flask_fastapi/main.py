"""
Aplicação principal — API de Biblioteca Virtual com FastAPI.

Este módulo define os endpoints da API e o ciclo de vida da aplicação.
Utiliza o padrão de Dependency Injection do FastAPI para gerenciar
sessões do banco de dados.

Endpoints:
    POST /livros/          → Cadastra um novo livro
    GET  /livros/          → Lista todos os livros
    GET  /livros/busca/    → Busca livros por título e/ou autor
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Book
from schemas import BookCreate, BookResponse
from seed import seed_db


# --- Ciclo de vida da aplicação (lifespan) ---
# O asynccontextmanager permite executar código na inicialização
# e no encerramento da aplicação.
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação:
    - Startup: cria as tabelas no banco e popula com dados iniciais.
    - Shutdown: (nenhuma ação necessária neste caso).
    """
    # Código executado na INICIALIZAÇÃO
    # Cria todas as tabelas definidas nos modelos (se não existirem)
    Base.metadata.create_all(bind=engine)

    # Popula o banco com dados iniciais
    db = Session(bind=engine)
    try:
        seed_db(db)
    finally:
        db.close()

    yield  # A aplicação roda aqui

    # Código executado no ENCERRAMENTO (cleanup)
    # Nada a fazer neste caso


# --- Instância da aplicação FastAPI ---
app = FastAPI(
    title="API Biblioteca Virtual",
    description="API para cadastro e consulta de livros em uma biblioteca virtual.",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Endpoints ---

@app.post("/livros/", response_model=BookResponse, status_code=201)
def criar_livro(livro: BookCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo livro na biblioteca.

    - **livro**: dados do livro no corpo da requisição (JSON).
    - O FastAPI valida automaticamente os campos usando o schema BookCreate.
    - Retorna o livro criado com o id gerado pelo banco.

    Args:
        livro (BookCreate): Dados do livro validados pelo Pydantic.
        db (Session): Sessão do banco injetada automaticamente pelo Depends.

    Returns:
        BookResponse: Livro criado com id.
    """
    # Converte o schema Pydantic para um objeto SQLAlchemy
    # model_dump() retorna um dicionário com os dados do schema
    # ** desempacota o dicionário como argumentos nomeados (kwargs)
    db_livro = Book(**livro.model_dump())

    db.add(db_livro)       # Adiciona o objeto à sessão (staged)
    db.commit()            # Persiste no banco de dados
    db.refresh(db_livro)   # Atualiza o objeto com os dados do banco (ex: id gerado)

    return db_livro


@app.get("/livros/", response_model=list[BookResponse])
def listar_livros(db: Session = Depends(get_db)):
    """
    Retorna todos os livros cadastrados na biblioteca.

    - A query `db.query(Book).all()` executa um SELECT * FROM books.
    - O response_model converte automaticamente os objetos ORM para JSON.

    Returns:
        list[BookResponse]: Lista de todos os livros.
    """
    livros = db.query(Book).all()
    return livros


@app.get("/livros/busca/", response_model=list[BookResponse])
def buscar_livros(
    titulo: str = Query(default=None, description="Texto para buscar no título"),
    autor: str = Query(default=None, description="Texto para buscar no autor"),
    db: Session = Depends(get_db),
):
    """
    Busca livros por título e/ou autor (busca parcial, case-insensitive).

    - Aceita os parâmetros de query `titulo` e `autor`, ambos opcionais.
    - Utiliza `ilike` (case-insensitive LIKE) para busca parcial.
    - Se ambos forem informados, aplica filtro AND (ambos devem corresponder).
    - Se nenhum for informado, retorna todos os livros.

    Exemplos de uso:
        GET /livros/busca/?titulo=dom
        GET /livros/busca/?autor=machado
        GET /livros/busca/?titulo=memorias&autor=machado

    Args:
        titulo (str, optional): Texto para buscar no título.
        autor (str, optional): Texto para buscar no autor.
        db (Session): Sessão do banco.

    Returns:
        list[BookResponse]: Lista de livros que correspondem à busca.
    """
    # Inicia a query base
    query = db.query(Book)

    # Aplica filtros condicionalmente
    # ilike = case-Insensitive LIKE
    # f"%{titulo}%" = busca parcial (contém o texto em qualquer posição)
    if titulo:
        query = query.filter(Book.titulo.ilike(f"%{titulo}%"))

    if autor:
        query = query.filter(Book.autor.ilike(f"%{autor}%"))

    resultados = query.all()
    return resultados
