# Questão 1 — API de Biblioteca Virtual

API REST para cadastro e consulta de livros, com dados pré-populados.

## Tecnologias

- **FastAPI** — Framework web para APIs
- **SQLAlchemy** — ORM para acesso ao banco
- **SQLite** — Banco de dados relacional (arquivo local)
- **Pydantic** — Validação de dados (entrada/saída)
- **Pytest** — Testes unitários

## Estrutura

```
├── main.py           # Endpoints e ciclo de vida da aplicação
├── database.py       # Configuração do banco (engine, sessão, dependency injection)
├── models.py         # Modelo ORM da tabela 'books'
├── schemas.py        # Schemas de validação (request/response)
├── seed.py           # 5 livros pré-populados na inicialização
├── test_main.py      # Testes unitários
└── requirements.txt  # Dependências
```

## Decisões Arquiteturais

- **Separação em módulos**: banco, modelo, schemas e seed em arquivos distintos para organização e manutenibilidade.
- **Dependency Injection** (`get_db` + `Depends`): cada request recebe sua própria sessão do banco, garantindo isolamento.
- **SessionLocal (fábrica de sessões)**: padrão recomendado pelo SQLAlchemy para gerenciar sessões por request.
- **Pydantic schemas separados do modelo ORM**: desacopla a estrutura da API do modelo do banco (padrão DTO).
- **Seed condicional**: livros inseridos apenas se o banco estiver vazio, evitando duplicatas.
- **Testes com banco em memória + StaticPool**: isolamento total dos testes sem afetar o banco real.

## Endpoints

| Método | Rota             | Descrição                          |
|--------|------------------|------------------------------------|
| POST   | `/livros/`       | Cadastra um novo livro             |
| GET    | `/livros/`       | Lista todos os livros              |
| GET    | `/livros/busca/` | Busca por `?titulo=...&autor=...`  |

## Como Executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# Documentação interativa: http://127.0.0.1:8000/docs
```

## Como Testar

```bash
pytest test_main.py -v
```
