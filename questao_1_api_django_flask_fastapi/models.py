"""
Módulo de modelos do banco de dados (ORM).

Define a estrutura da tabela 'books' usando SQLAlchemy.
Cada classe que herda de Base representa uma tabela no banco.
Os atributos da classe representam as colunas da tabela.
"""

from sqlalchemy import Column, Integer, String, Text
from database import Base


class Book(Base):
    """
    Modelo que representa um livro na biblioteca virtual.

    Atributos:
        id (int): Chave primária, auto-incrementada pelo banco.
        titulo (str): Título do livro (obrigatório, indexado para buscas rápidas).
        autor (str): Nome do autor (obrigatório, indexado para buscas rápidas).
        data_publicacao (str): Data de publicação no formato 'YYYY-MM-DD'.
        resumo (str): Resumo/sinopse do livro (campo de texto longo).

    O parâmetro `index=True` cria um índice no banco de dados para
    acelerar buscas por título e autor.
    """

    # Nome da tabela no banco de dados
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False, index=True)
    autor = Column(String, nullable=False, index=True)
    data_publicacao = Column(String, nullable=False)
    resumo = Column(Text, nullable=False)
