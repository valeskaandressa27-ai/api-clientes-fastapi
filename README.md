# Customer Management Dashboard
🚀 Aplicação online:
https://api-clientes-fastapi-1.onrender.com
Sistema full-stack de gestão de clientes: back-end **FastAPI + PostgreSQL**
e front-end **Vue 3 + TypeScript**, publicados como **uma única aplicação**
(o FastAPI serve tanto a API REST quanto os arquivos estáticos do Vue).

## Sumário

- [Visão geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Endpoints da API](#endpoints-da-api)
- [Rodando localmente](#rodando-localmente)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Banco de dados e migrations](#banco-de-dados-e-migrations)
- [Testes](#testes)
- [Docker](#docker)
- [Deploy no Render (aplicação única)](#deploy-no-render-aplicação-única)
- [Segurança](#segurança)
- [Decisões técnicas](#decisões-técnicas)

## Visão geral

O projeto nasceu como uma API de clientes (FastAPI) e foi expandido para um
sistema completo com interface web: dashboard com métricas, listagem de
clientes com busca e paginação, cadastro, edição, detalhes e exclusão — tudo
consumindo a API REST real, sem dados mockados.

## Tecnologias

**Back-end**
- Python 3.12+, FastAPI, Uvicorn
- PostgreSQL, SQLAlchemy 2.x, Alembic, psycopg
- Pydantic 2.x
- pytest + HTTPX

**Front-end**
- Vue 3 (Composition API) + TypeScript
- Vite
- Vue Router 4
- CSS puro (design system próprio, sem framework de UI)

## Arquitetura

```
/
├── app/                    # Back-end FastAPI
│   ├── core/               # Configurações e exceções de domínio
│   ├── database/           # Engine e sessão do SQLAlchemy
│   ├── models/              # Modelos ORM
│   ├── repositories/       # Acesso a dados
│   ├── routes/             # Rotas REST (clientes, dashboard, health)
│   ├── schemas/            # Schemas Pydantic
│   ├── services/           # Regras de negócio
│   └── main.py             # App FastAPI + serve o build do Vue em produção
│
├── frontend/               # Front-end Vue 3 + TypeScript
│   ├── src/
│   │   ├── components/     # Sidebar, modal de confirmação, toasts
│   │   ├── views/           # Dashboard, Clientes, Detalhe, Formulário
│   │   ├── router/          # Vue Router
│   │   ├── services/        # Cliente HTTP centralizado (api.ts)
│   │   ├── composables/     # useToast (feedback de ações)
│   │   ├── utils/           # Formatação de CPF, telefone, datas
│   │   └── styles/          # Design tokens e estilos globais
│   ├── package.json
│   ├── vite.config.ts       # Proxy de /api para o back-end em dev
│   └── dist/                # Gerado pelo build (não versionado)
│
├── tests/                   # Testes automatizados (pytest + HTTPX)
├── alembic/                 # Migrations
├── Dockerfile                # Multi-stage: build do Vue + runtime Python
├── requirements.txt
└── .env.example
```

Fluxo de uma requisição da API: **routes → services → repositories → models**.
O front-end nunca acessa o banco diretamente — tudo passa pela API REST.

## Funcionalidades

**Dashboard**
- Total de clientes, novos cadastros nos últimos 7 e 30 dias
- Gráfico de cadastros nos últimos 6 meses
- Lista de clientes recentes
- Todos os números vêm de um endpoint dedicado (`/api/dashboard/resumo`),
  calculados a partir dos dados reais — nenhuma métrica é inventada no
  front-end.

**Clientes**
- Listagem com busca por nome (debounce), paginação, tabela responsiva
- Cadastro e edição com validação client-side (CPF, e-mail, telefone) e
  tratamento dos erros retornados pelo back-end (422 e 409)
- Página de detalhes com dados completos do cliente
- Exclusão com modal de confirmação
- Estados de carregamento, erro, vazio e sucesso (toasts) em todas as telas
- Layout responsivo: sidebar recolhível em telas pequenas, tabela adaptada
  em cards em telas estreitas

## Endpoints da API

Todas as rotas de clientes e dashboard estão sob o prefixo `/api` — isso
evita colisão com as rotas do front-end (por exemplo, `/clientes` é uma
página do Vue, enquanto `/api/clientes` é o endpoint da API). Veja mais em
[Decisões técnicas](#decisões-técnicas).

| Método | Endpoint                  | Descrição                          |
|--------|----------------------------|-------------------------------------|
| POST   | /api/clientes              | Criar cliente                       |
| GET    | /api/clientes              | Listar clientes (busca + paginação) |
| GET    | /api/clientes/{id}         | Buscar cliente                      |
| PUT    | /api/clientes/{id}         | Atualizar cliente                   |
| DELETE | /api/clientes/{id}         | Excluir cliente                     |
| GET    | /api/dashboard/resumo      | Métricas agregadas para o dashboard |
| GET    | /health                    | Verificar API                       |
| GET    | /docs                       | Swagger UI                          |
| GET    | /redoc                      | ReDoc                               |

Códigos de status preservados: `201` (criação), `200` (sucesso), `204`
(exclusão), `404` (não encontrado), `409` (e-mail/CPF duplicado), `422`
(dados inválidos), `500` (erro inesperado, sem detalhes internos expostos).

## Rodando localmente

Você pode rodar back-end e front-end separadamente (recomendado para
desenvolver) ou testar o build de produção completo.

### 1. Back-end

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edite o .env com os dados do seu PostgreSQL local

alembic upgrade head
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000` (Swagger em `/docs`).

### 2. Front-end (modo desenvolvimento)

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

O Vite sobe em `http://localhost:5173` e encaminha automaticamente qualquer
chamada a `/api/*` para `http://localhost:8000` (configurado em
`vite.config.ts`), então não é preciso configurar CORS manualmente em
desenvolvimento nem definir `VITE_API_URL`.

### 3. Build de produção completo (opcional, para testar como no Render)

```bash
cd frontend && npm install && npm run build && cd ..
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Acesse `http://localhost:8000` — o FastAPI vai servir o Vue já compilado a
partir de `frontend/dist`.

## Variáveis de ambiente

**Back-end** (`.env`, veja `.env.example`)

| Variável       | Descrição                                          |
|----------------|------------------------------------------------------|
| `DATABASE_URL` | String de conexão do PostgreSQL                      |
| `CORS_ORIGINS` | Origens extras permitidas (útil em dev, opcional em produção same-origin) |
| `ENVIRONMENT`  | `development` ou `production`                        |

**Front-end** (`frontend/.env`, veja `frontend/.env.example`)

| Variável        | Descrição                                                        |
|------------------|--------------------------------------------------------------------|
| `VITE_API_URL`   | Opcional. Deixe vazio para usar a própria origem (produção) ou o proxy do Vite (dev). |

Nunca versione `.env` — ambos já estão no `.gitignore`.

## Banco de dados e migrations

PostgreSQL + Alembic, como no projeto original.

```bash
alembic upgrade head                                  # aplicar migrations
alembic revision --autogenerate -m "descrição"        # criar nova migration
alembic downgrade -1                                  # reverter a última
```

## Testes

```bash
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/clientes_test"
pytest -v
```

16 testes cobrindo: CRUD de clientes (válido/inválido, paginação, busca,
404, duplicidade de e-mail/CPF) e as métricas do dashboard (com e sem
clientes cadastrados).

## Docker

O `Dockerfile` é multi-stage:

1. **Stage `frontend-build`** (`node:20-slim`): instala as dependências do
   Vue com `npm ci` e roda `npm run build`, gerando `frontend/dist`.
2. **Stage `runtime`** (`python:3.12-slim`): instala as dependências
   Python, copia o código do back-end e copia o `frontend/dist` gerado no
   stage anterior. Ao iniciar, roda `alembic upgrade head` e depois
   `uvicorn`, respeitando a variável `PORT` do ambiente (com fallback para
   `8000` fora do Render).

Build e execução local (requer Docker instalado):

```bash
docker build -t customer-management-dashboard .
docker run -p 8000:8000 --env-file .env customer-management-dashboard
```

## Deploy no Render (aplicação única)

Um único Web Service, sem Vercel e sem repositórios separados:

1. Suba este projeto (como está, com a pasta `frontend/` incluída) para um
   repositório no GitHub.
2. No Render, crie um **Web Service** apontando para o repositório e
   escolha o ambiente **Docker** — o `Dockerfile` é detectado
   automaticamente e cuida de todo o build (Node + Python).
3. Crie uma instância de **PostgreSQL** no Render (ou use um banco externo).
4. Configure as variáveis de ambiente do Web Service:
   - `DATABASE_URL`: a *Internal Database URL* do Postgres do Render,
     trocando o prefixo `postgresql://` por `postgresql+psycopg://`
   - `CORS_ORIGINS`: pode deixar o padrão, já que front-end e API são
     servidos pela mesma origem em produção
   - `ENVIRONMENT=production`
5. **Não defina `VITE_API_URL`** no Web Service — variáveis `VITE_*` são
   usadas apenas durante o *build* do front-end (stage 1 do Dockerfile) e,
   deixando-a vazia, o Vue usa a própria origem automaticamente, que é o
   comportamento correto em produção.
6. Não configure porta fixa: o `CMD` do Dockerfile já lê `$PORT`, que o
   Render injeta automaticamente.
7. Deploy. Nos logs, confirme que `alembic upgrade head` rodou sem erro e
   que apareceu "Your service is live".
8. Verifique:
   - `https://<seu-servico>.onrender.com/health` → `{"status":"ok"}`
   - `https://<seu-servico>.onrender.com/` → Dashboard do Vue
   - `https://<seu-servico>.onrender.com/docs` → Swagger da API

## Segurança

- Nenhuma credencial no código-fonte; `.env` (back-end) e `frontend/.env`
  (front-end) estão no `.gitignore`.
- Toda entrada é validada via Pydantic (back-end) e revalidada no front-end
  apenas para UX — o back-end é sempre a autoridade final.
- Mensagens de erro não expõem detalhes internos (stack traces, queries).
- CORS restrito às origens definidas em `CORS_ORIGINS`; em produção,
  front-end e API compartilham a mesma origem, então CORS entre eles nem
  entra em jogo.
- Autenticação/JWT continua fora do escopo desta versão, como no back-end
  original.

## Decisões técnicas

**Por que a API ficou sob `/api`?**
No projeto original, os endpoints de clientes viviam em `/clientes`. Ao
adicionar um front-end com Vue Router, a página de listagem de clientes
também precisa de uma rota `/clientes`. Se a API mantivesse o mesmo
caminho, uma pessoa recarregando a página `/clientes` no navegador cairia
na resposta JSON da API em vez de na aplicação Vue. Prefixar a API com
`/api` resolve esse conflito sem alterar nenhum comportamento, validação ou
contrato de dados — apenas o caminho base mudou.

**Como o FastAPI serve o Vue?**
Em produção, `app/main.py` monta os arquivos de `frontend/dist/assets` como
arquivos estáticos e usa uma rota "catch-all" que devolve `index.html` para
qualquer caminho que não seja uma rota de API conhecida — é o padrão usual
para servir uma SPA (Single Page Application) a partir de um back-end,
permitindo que o Vue Router controle a navegação no navegador enquanto o
FastAPI apenas entrega o arquivo inicial.

**Por que não usei Vuex/Pinia?**
O estado da aplicação é simples o bastante (dados por página, buscados sob
demanda) para não precisar de uma store global — cada view busca o que
precisa diretamente do `services/api.ts`. Isso mantém o projeto enxuto sem
abrir mão de organização.
