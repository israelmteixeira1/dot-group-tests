"""
Módulo de schemas Pydantic para validação e serialização de dados.

Os schemas definem o formato dos dados que entram (request) e saem (response)
da API. O Pydantic valida automaticamente os tipos e campos obrigatórios.

- BookCreate: schema de entrada para criação de livros.
- BookResponse: schema de saída com o id incluído.
"""

from pydantic import BaseModel


class BookCreate(BaseModel):
    """
    Schema para criação de um novo livro (corpo do POST).

    Todos os campos são obrigatórios. O Pydantic retorna erro 422
    automaticamente se algum campo estiver faltando ou com tipo errado.
    """
    titulo: str
    autor: str
    data_publicacao: str
    resumo: str


class BookResponse(BookCreate):
    """
    Schema de resposta (retorno da API).

    Herda todos os campos de BookCreate e adiciona o 'id'.
    O model_config com from_attributes=True permite que o Pydantic
    leia os dados diretamente de objetos SQLAlchemy (modo ORM).
    """
    id: int

    # Configuração que permite converter objetos ORM (SQLAlchemy)
    # para o schema Pydantic automaticamente.
    # Antes do Pydantic v2, isso era feito com:
    #   class Config:
    #       orm_mode = True
    model_config = {"from_attributes": True}
