# API de Gerenciamento de Clientes

## Descrição

API REST para cadastro, consulta, atualização e exclusão (CRUD) de clientes,
construída com **FastAPI** e **PostgreSQL**. Projeto de portfólio focado em
demonstrar boas práticas de desenvolvimento de APIs em Python: validação de
dados, tratamento de erros, migrations, testes automatizados e organização em
camadas.

## Tecnologias

- Python 3.12+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy 2.x
- Pydantic 2.x
- Alembic (migrations)
- psycopg (driver PostgreSQL)
- pytest + HTTPX (testes)
- Docker

## Funcionalidades

- Cadastro de clientes com validação de nome, e-mail, telefone e CPF
- Listagem de clientes com paginação e busca por nome/e-mail
- Busca de cliente por ID
- Atualização de cliente
- Exclusão de cliente
- Bloqueio de e-mail e CPF duplicados
- Tratamento consistente de erros (404, 409, 422, 500)
- Documentação automática via Swagger (`/docs`) e ReDoc (`/redoc`)
- Health check (`/health`)
- CORS configurável por variável de ambiente

## Arquitetura

O projeto segue uma separação em camadas, cada uma com responsabilidade única:

```
app/
├── main.py            # Criação do app, middlewares e exception handlers
├── core/
│   ├── config.py      # Configurações via variáveis de ambiente
│   └── exceptions.py  # Exceções de domínio (não acopladas ao FastAPI)
├── database/
│   └── session.py     # Engine, sessão e Base declarativa do SQLAlchemy
├── models/
│   └── cliente.py     # Modelo ORM da tabela `clientes`
├── schemas/
│   └── cliente.py     # Schemas Pydantic + validações (e-mail, CPF, telefone)
├── repositories/
│   └── cliente.py      # Acesso direto ao banco de dados (queries)
├── services/
│   └── cliente.py      # Regras de negócio (duplicidade, orquestração)
└── routes/
    ├── clientes.py      # Endpoints REST de clientes
    └── health.py        # Endpoint de health check
```

Fluxo de uma requisição: **routes → services → repositories → models**.
As rotas nunca acessam o banco diretamente; toda regra de negócio (como
verificação de duplicidade) fica nos services.

## Endpoints

| Método | Endpoint          | Descrição            |
|--------|-------------------|-----------------------|
| POST   | /clientes         | Criar cliente         |
| GET    | /clientes         | Listar clientes       |
| GET    | /clientes/{id}    | Buscar cliente        |
| PUT    | /clientes/{id}    | Atualizar cliente     |
| DELETE | /clientes/{id}    | Excluir cliente       |
| GET    | /health           | Verificar API         |

`GET /clientes` aceita os parâmetros de query `pagina`, `tamanho_pagina`,
`nome` e `email` para paginação e busca.

## Instalação local

```bash
# 1. Criar e ativar um ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Copiar o arquivo de variáveis de ambiente
cp .env.example .env
# edite o .env com os dados do seu PostgreSQL local

# 4. Executar as migrations
alembic upgrade head

# 5. Iniciar a aplicação
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

## Variáveis de ambiente

| Variável       | Descrição                                            | Exemplo                                                        |
|----------------|-------------------------------------------------------|-----------------------------------------------------------------|
| `DATABASE_URL` | String de conexão do PostgreSQL                       | `postgresql+psycopg://usuario:senha@host:5432/clientes`         |
| `CORS_ORIGINS` | Origens permitidas para CORS, separadas por vírgula   | `http://localhost:5173,https://meuapp.com`                      |
| `ENVIRONMENT`  | Ambiente de execução                                  | `development` ou `production`                                   |

Nunca versione o arquivo `.env` — use sempre `.env.example` como referência.

## Banco de dados e migrations

O projeto usa **Alembic** para gerenciar o schema do PostgreSQL; a tabela
`clientes` nunca deve ser criada manualmente.

```bash
# Aplicar todas as migrations pendentes
alembic upgrade head

# Criar uma nova migration a partir de alterações nos models
alembic revision --autogenerate -m "descrição da alteração"

# Reverter a última migration
alembic downgrade -1
```

## Testes

Os testes usam um banco PostgreSQL de teste dedicado (definido por
`DATABASE_URL` no momento da execução) e criam/derrubam as tabelas a cada
teste, isoladamente.

```bash
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/clientes_test"
pytest -v
```

Cobertura: criação (válida e inválida), listagem, paginação, busca por ID,
cliente inexistente, atualização, exclusão, e-mail duplicado e CPF duplicado.

## Swagger / ReDoc

Com a aplicação em execução:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deploy no Render

1. Suba o projeto para um repositório no GitHub.
2. No Render, crie um novo **Web Service** apontando para o repositório.
3. Escolha o ambiente **Docker** (o `Dockerfile` já está pronto — o Render o
   detecta automaticamente).
   - Build command: não é necessário (o Docker cuida do build).
   - Start command: não é necessário (definido no `CMD` do Dockerfile).
   - Alternativamente, sem Docker: build command `pip install -r
     requirements.txt` e start command
     `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Crie uma instância de **PostgreSQL** no Render (ou use um banco externo).
5. Configure as variáveis de ambiente do serviço:
   - `DATABASE_URL` (o Render fornece a Internal Connection String do banco criado)
   - `CORS_ORIGINS` com o domínio do seu front-end
   - `ENVIRONMENT=production`
6. Faça o deploy. As migrations rodam automaticamente no start (`CMD` do
   Dockerfile executa `alembic upgrade head` antes do Uvicorn).
7. Verifique `https://<seu-servico>.onrender.com/health` — deve retornar
   `{"status": "ok"}`.
8. Acesse `https://<seu-servico>.onrender.com/docs` para conferir o Swagger.

## Segurança

- Nenhuma credencial é armazenada no código-fonte.
- O `.env` está no `.gitignore` e nunca deve ser versionado.
- Toda entrada é validada via Pydantic antes de chegar ao banco.
- Todo acesso a dados passa pelo SQLAlchemy (sem SQL manual concatenado).
- Mensagens de erro não expõem detalhes internos (stack traces, queries etc.).
- CORS é restrito às origens definidas em `CORS_ORIGINS`.
- Autenticação/JWT foi propositalmente deixada fora desta primeira versão.
