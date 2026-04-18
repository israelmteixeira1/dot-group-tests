"""
Módulo de seed (dados iniciais) do banco de dados.

Contém uma lista de livros clássicos da literatura brasileira
que são inseridos automaticamente na inicialização da aplicação,
caso o banco esteja vazio.
"""

from sqlalchemy.orm import Session
from models import Book


# Lista de livros pré-populados
LIVROS_INICIAIS = [
    {
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "data_publicacao": "1899-01-01",
        "resumo": "Romance que narra a história de Bentinho e Capitu, "
                  "explorando temas como ciúme, dúvida e traição. "
                  "Considerado uma das obras-primas da literatura brasileira."
    },
    {
        "titulo": "Grande Sertão: Veredas",
        "autor": "Guimarães Rosa",
        "data_publicacao": "1956-01-01",
        "resumo": "Épico sertanejo que acompanha o jagunço Riobaldo em suas "
                  "aventuras e reflexões filosóficas pelo sertão mineiro. "
                  "Obra inovadora pela linguagem e estrutura narrativa."
    },
    {
        "titulo": "O Cortiço",
        "autor": "Aluísio Azevedo",
        "data_publicacao": "1890-01-01",
        "resumo": "Romance naturalista que retrata a vida em um cortiço "
                  "no Rio de Janeiro, abordando as condições sociais e "
                  "as relações humanas da época."
    },
    {
        "titulo": "Memórias Póstumas de Brás Cubas",
        "autor": "Machado de Assis",
        "data_publicacao": "1881-01-01",
        "resumo": "Narrado por um defunto autor, o romance apresenta "
                  "as memórias de Brás Cubas com ironia e pessimismo, "
                  "inaugurando o Realismo na literatura brasileira."
    },
    {
        "titulo": "Capitães da Areia",
        "autor": "Jorge Amado",
        "data_publicacao": "1937-01-01",
        "resumo": "Romance que retrata a vida de um grupo de meninos "
                  "de rua em Salvador, liderados por Pedro Bala, "
                  "abordando temas como pobreza, injustiça social e liberdade."
    },
]


def seed_db(db: Session):
    """
    Popula o banco com os livros iniciais.

    Verifica se já existem livros no banco antes de inserir,
    evitando duplicatas em reinicializações da aplicação.

    Args:
        db (Session): sessão ativa do banco de dados.
    """
    # Conta quantos livros já existem no banco
    count = db.query(Book).count()

    if count == 0:
        # Cria objetos Book a partir dos dicionários e insere no banco
        for livro_data in LIVROS_INICIAIS:
            livro = Book(**livro_data)  # Desempacota o dicionário como kwargs
            db.add(livro)

        db.commit()
        print(f"✅ Banco populado com {len(LIVROS_INICIAIS)} livros iniciais.")
    else:
        print(f"ℹ️  Banco já contém {count} livros. Seed ignorado.")
