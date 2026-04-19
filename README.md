# dot-group-tests
Testes técnicos para desenvolvedor backend com foco em IA. Este projeto está dividido em pastas, cada uma contendo a solução de uma questão específica do teste.

---

## Questão 1 — API de Biblioteca Virtual
API REST para cadastro e consulta de livros, com dados pré-populados utilizando banco de dados SQLite local. Arquitetura baseada em endpoints com injeção de dependência e validação Pydantic.

### Tecnologias
- FastAPI, SQLAlchemy, SQLite, Pydantic, Pytest

### Como Executar
```bash
cd questao_1_api_django_flask_fastapi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Acesse a documentação interativa em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Testes**
Para validar, no mesmo diretório execute: `pytest test_main.py -v`

---

## Questão 2 — Chatbot com IA Generativa
Chatbot conversacional diretamente no terminal. Utiliza o fluxo do LangChain juntamente com a API da OpenAI. Foi implementada uma memória (`ConversationBufferMemory`) para que o bot tenha contexto das mensagens ao longo da conversa.

### Tecnologias
- Python, LangChain, OpenAI API, python-dotenv

### Como Executar
```bash
cd questao_2_chatbot_ia_generativa
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Antes de executar, configure sua chave da OpenAI copiando o arquivo de exemplo:
```bash
cp .env.example .env
```
*(Edite o `.env` incluindo sua `OPENAI_API_KEY` válida)*

Execute o chatbot:
```bash
python chatbot.py
```

### Imagens de Exemplo
Imagens demonstrando interações do usuário com o chatbot e o monitoramento pela ferramenta do LangSmith estão localizadas no diretório [`questao_2_chatbot_ia_generativa/exemple-questions/`](./questao_2_chatbot_ia_generativa/exemple-questions/).

---

## Questão 3 — Vector Stores e Embeddings
*(Em desenvolvimento...)*
