"""
Módulo de configuração do banco de dados.

Utiliza SQLAlchemy como ORM para gerenciar a conexão com o banco SQLite.
- `engine`: objeto que gerencia a conexão com o banco de dados.
- `SessionLocal`: fábrica de sessões — cada chamada gera uma sessão independente.
- `Base`: classe base declarativa para definição dos modelos (tabelas).
- `get_db()`: dependency injection do FastAPI para fornecer uma sessão por request.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o banco SQLite (arquivo local 'biblioteca.db')
# O parâmetro connect_args={"check_same_thread": False} é necessário
# para o SQLite funcionar com múltiplas threads do FastAPI.
SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# sessionmaker cria uma "fábrica" de sessões configurada com o engine.
# autocommit=False: transações precisam ser commitadas manualmente.
# autoflush=False: evita flushes automáticos antes de queries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa — todos os modelos herdam desta classe
# para que o SQLAlchemy saiba quais tabelas criar.
Base = declarative_base()


def get_db():
    """
    Dependency injection para endpoints do FastAPI.

    Cria uma sessão (conexão) com o banco no início da request
    e a fecha automaticamente ao final, garantindo que recursos
    não fiquem abertos desnecessariamente.

    Uso no endpoint:
        def endpoint(db: Session = Depends(get_db)):
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
