# Ingestão e Busca Semântica com LangChain e Postgres

Software que lê um PDF, armazena seu conteúdo vetorizado em PostgreSQL (com pgVector) e permite
fazer perguntas sobre esse conteúdo via linha de comando. Responde **somente** com base no que
está no PDF — se a informação não estiver no documento, responde que não tem informações
suficientes.

Suporta dois provedores de IA, configuráveis via `.env`: **OpenAI** ou **Google Gemini**.

## Estrutura

```
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── config.py     # Configuração/seleção de provedor (OpenAI ou Gemini)
│   ├── ingest.py     # Script de ingestão do PDF
│   ├── search.py     # Busca semântica no pgVector
│   ├── chat.py        # CLI de perguntas e respostas
├── document.pdf       # PDF a ser ingerido (adicione o seu)
└── README.md
```

## Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Uma API key da OpenAI **ou** da Google (Gemini)

## Configuração

1. Crie e ative um ambiente virtual:

   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e preencha:

   ```powershell
   Copy-Item .env.example .env
   ```

   - Defina `AI_PROVIDER` como `openai` ou `gemini`.
   - Preencha `OPENAI_API_KEY` (se usar OpenAI) ou `GOOGLE_API_KEY` (se usar Gemini).

4. Coloque o PDF que será consultado na raiz do projeto como `document.pdf`
   (ou ajuste `PDF_PATH` no `.env`).

## Execução

1. Subir o banco de dados (PostgreSQL + pgVector):

   ```powershell
   docker compose up -d
   ```

2. Executar a ingestão do PDF:

   ```powershell
   python src/ingest.py
   ```

3. Rodar o chat:

   ```powershell
   python src/chat.py
   ```

### Exemplo de uso

```
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.
```

```
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Digite `sair` para encerrar o chat.

## Detalhes técnicos

- O PDF é dividido em chunks de **1000 caracteres** com **150 de overlap**
  (`RecursiveCharacterTextSplitter`).
- Embeddings:
  - OpenAI: `text-embedding-3-small`
  - Gemini: `models/embedding-001`
- LLM de resposta:
  - OpenAI: `gpt-5-nano`
  - Gemini: `gemini-2.5-flash-lite`
- Busca por similaridade retorna os **10 resultados mais relevantes** (`k=10`), concatenados
  como contexto no prompt enviado à LLM.
