# dot-group-tests
Teste técnico backend/IA com três soluções independentes: (1) API REST de biblioteca virtual com FastAPI + SQLAlchemy + Pytest; (2) chatbot terminal com LangChain + OpenAI API + ConversationBufferMemory; (3) pipeline RAG com extração de PDF, chunking, embeddings via Sentence Transformers e indexação vetorial com FAISS.
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

Este tema tem relevância direta com o meu TCC da pós-graduação em **Inteligência Artificial Aplicada**: um processo de otimização em um projeto já existente, utilizando aplicações RAG (*Retrieval-Augmented Generation*) e suas variantes, técnicas de engenharia de prompt, fine-tuning e outras abordagens na obtenção de respostas sobre a pecuária leiteira. A questão foi uma oportunidade de aplicar na prática conceitos que estou estudando e desenvolvendo academicamente.

Sistema de busca semântica de documentos que indexa o conteúdo do livro **"500 Perguntas 500 Respostas — Gado de Leite" (Embrapa, 2012)** em um banco vetorial FAISS e permite consultas em linguagem natural. O texto é extraído do PDF, fatiado em chunks, convertido em vetores de embeddings e persistido em disco — nas execuções seguintes o índice é carregado diretamente, sem reprocessar o arquivo.

### Tecnologias
- Python, LangChain, FAISS, HuggingFace Sentence Transformers, pdfplumber

### Como Executar
```bash
cd questao_3_vector_stores_embeddings
pip install -r requirements.txt
python busca_semantica.py
```

> **Nota:** `numpy==1.26.4` é um pin intencional — `faiss-cpu 1.7.4` quebra com NumPy 2.x.

Na primeira execução o PDF é processado e o índice FAISS é construído e salvo em `faiss_index/`. As execuções seguintes carregam o índice do disco diretamente.

O script exibe automaticamente 5 consultas de demonstração e em seguida entra em modo interativo, onde é possível digitar qualquer pergunta em linguagem natural. Digite `sair` para encerrar.

### Imagem de Exemplo
[`exemple-questions.png`](./questao_3_vector_stores_embeddings/exemple-questions.png) — demonstração do sistema em execução com exemplos de consultas e os trechos retornados pelo índice semântico.
