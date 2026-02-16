# PhiloAgents

A from-scratch reimplementation of an end-to-end AI pipeline inspired by [neural-maze/philoagents-course](https://github.com/neural-maze/philoagents-course/). The goal is to deeply understand data ingestion, modeling, evaluation, and deployment trade-offs.

---

## What it does

PhiloAgents is an AI agent simulation engine that impersonates historical philosophers (Plato, Aristotle, Turing, Descartes, etc.) in conversational form. Users chat with philosopher personas powered by LLMs, RAG over curated knowledge bases, and persistent memory—all exposed via a REST API.

---

## Key features I built

- **Agentic RAG pipeline** — LangGraph workflow with retrieval-augmented generation over Wikipedia + Stanford Encyclopedia of Philosophy
- **Short- and long-term memory** — MongoDB-backed state checkpoints and long-term memory with hybrid search
- **REST API** — FastAPI with `/chat` and `/reset_memory` endpoints
- **Evaluation pipeline** — LLM-as-judge evaluation (Opik) with hallucination, relevance, moderation, context recall/precision metrics
- **Prompt versioning** — Opik integration for tracking and versioning prompts
- **Docker-first setup** — Reproducible dev environment with MongoDB Atlas Local + API container

---

## What I learned

- End-to-end agent design: data extraction → chunking → embeddings → retrieval → generation
- Trade-offs between local vs. cloud LLMs, embedding models, and RAG chunk sizes
- Evaluation design: dataset construction, metric selection, and experiment tracking
- Production concerns: checkpointing, memory limits, summarization, and API ergonomics

---

## How to run / demo

**Prerequisites:** Docker, Docker Compose. For `create-long-term-memory` (non-Docker): [uv](https://docs.astral.sh/uv/).

1. **Clone and configure**
   ```bash
   git clone <repo-url>
   cd philoagents
   cp philoagents-api/.env.example philoagents-api/.env
   ```
   Edit `philoagents-api/.env` and set `GROQ_API_KEY` and `OPENAI_API_KEY` (required). Add `COMET_API_KEY` and `COMET_WORKSPACE` for evaluation/LLMOps.

2. **Start infrastructure**
   ```bash
   make infrastructure-api-up
   ```
   Brings up MongoDB and the API. API is available at `http://localhost:8000`.

3. **Populate long-term memory** (one-time)
   ```bash
   make create-long-term-memory        # requires uv
   # or
   make create-long-term-memory-docker  # runs in Docker
   ```
   Ingests and indexes philosopher knowledge into MongoDB.

4. **Chat**
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is consciousness?", "philosopher_id": "turing"}'
   ```

5. **Evaluate** (optional, requires Comet/Opik keys)
   ```bash
   make evaluate-agent
   ```

---

## Project structure

```
philoagents/
├── philoagents-api/          # Backend (Python)
│   ├── src/philoagents/
│   │   ├── application/      # RAG, memory, conversation, evaluation
│   │   ├── domain/           # Philosopher definitions, prompts
│   │   └── infrastructure/   # API, MongoDB, Opik
│   └── tools/                # Scripts: create_long_term_memory, evaluate_agent
├── docker-compose.yml
└── makefile
```
