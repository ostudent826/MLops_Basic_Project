# AI Platform — Production LLM Infrastructure

> A production-grade AI platform built from scratch over 6 months, evolving from a simple HTTP client to a fully deployed, multi-tenant AI gateway on GCP Cloud Run.

---

## What This Is

This project is a real-world AI infrastructure platform built as part of a structured 6-month self-directed study plan. The goal: bridge from DevOps/Network Engineering into AI Platform Engineering — applying existing knowledge of API gateways, load balancers, and cloud infrastructure to the LLM operations space.

Every module was built intentionally, with production concerns in mind from day one: security, observability, cost control, and reliability.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FastAPI Service                    │
│           /health  /chat  /query  /metrics           │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                  Security Layer                      │
│     Rate limiting · Input validation · Auth          │
│          Prompt injection detection · PII            │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                  Gateway Layer                       │
│   Multi-provider routing (Anthropic → Gemini →       │
│   OpenAI) · Fallback chains · Cost tracking ·        │
│          Budget circuit breaker                      │
└─────────────┬─────────────────────┬─────────────────┘
              │                     │
┌─────────────▼──────────┐ ┌───────▼─────────────────┐
│      LLM Clients        │ │      RAG Layer           │
│  Anthropic · LiteLLM   │ │  Embeddings · ChromaDB   │
│  Vertex AI (GCP)       │ │  Chunker · Retrieval     │
└────────────────────────┘ └─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                 Observability                        │
│  Structured JSON logging · Trace IDs · Metrics ·     │
│              Cost per request                        │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│              GCP Cloud Run                           │
│   Docker · Secret Manager · Cloud Monitoring         │
└─────────────────────────────────────────────────────┘
```

---

## Key Features

### 🔀 Multi-Provider LLM Gateway
- Provider-agnostic routing via **LiteLLM**
- Automatic failover chain: Anthropic → Gemini → OpenAI
- Exception translation so the router stays decoupled from provider-specific errors
- Analogous to an F5/NetScaler pool with health-check-driven failover

### 💰 AI FinOps / Budget Circuit Breaker
- Per-request cost tracking with configurable budgets
- Soft limit (warn at 80%) and hard limit (block at 100%)
- `BudgetExceededError` bypasses the fallback chain — runaway spend stopped at the gate
- The problem this solves: a developer loop calling GPT-4 overnight can cost $500+. This doesn't let that happen.

### 🛡️ Security Layer
- Sliding window rate limiter
- Token limit enforcement (pre-flight check)
- Prompt injection pattern blocklist (analogous to WAF rules in Apigee)
- Input validation before any LLM call is made

### 📦 RAG Pipeline (Retrieval-Augmented Generation)
- Document chunker with guard clause validation
- Embedding generation with result caching
- ChromaDB vector store wrapper
- Full pipeline: Query → Retrieve relevant chunks → Augment prompt → Generate grounded answer

### 🔍 Observability
- Structured JSON logging (environment-aware: JSON in prod, human-readable in dev)
- Request IDs on every log line (same concept as `X-Request-ID` in Apigee)
- Token usage and cost logged per request

### ⚙️ Configuration
- Pydantic `BaseSettings` with YAML support
- Nested config (`AnthropicSettings`, etc.)
- Environment variables take priority — same override hierarchy as Terraform/K8s ConfigMaps

---

## Project Structure

```
MLops_Project/
└── src/
    └── ai_platform/
        ├── api/
        │   └── router/
        │       └── v1.py          # FastAPI endpoints (/health, /chat)
        ├── gateway/
        │   ├── llm_clients.py     # LiteLLM wrapper + exception translation
        │   ├── llm_router.py      # Multi-provider failover chain
        │   └── cost.py            # Cost tracking + budget circuit breaker
        ├── llm/
        │   └── client.py          # Anthropic SDK wrapper
        ├── retrieval/
        │   ├── chunker.py         # Document chunking
        │   └── embeddings.py      # Embedding generation + caching
        ├── security/
        │   └── validation.py      # Rate limiting, token limits, injection detection
        ├── config.py              # Pydantic BaseSettings + YAML config
        ├── config.yaml            # Base configuration
        ├── exceptions.py          # Custom exceptions (BudgetExceededError, etc.)
        ├── http_client.py         # Resilient HTTP client with retry + backoff
        └── logger.py              # Structured JSON logger
```

---

## Tech Stack

| Category | Tool | Why |
|---|---|---|
| API Framework | FastAPI | Async-native, Pydantic integration, auto-docs |
| LLM Providers | Anthropic, Gemini, OpenAI | Multi-provider via LiteLLM |
| LLM Gateway | LiteLLM | Provider abstraction + fallback routing |
| Vector DB | ChromaDB | Simple, local-first, no infra overhead |
| Config/Validation | Pydantic v2 + PyYAML | Schema validation + typed settings |
| Testing | pytest | Standard, powerful |
| Cloud | GCP Cloud Run | Scales to zero, long timeouts, known ecosystem |
| IaC | Terraform | Infrastructure as code for GCP resources |

---

## Background & Motivation

I come from a network/infrastructure background — API gateways (Apigee), load balancers (NetScaler, F5), GCP networking, Kubernetes, Terraform. The AI ecosystem moves fast, but the underlying infrastructure problems are the same ones I've been solving for years:

- How do you route traffic intelligently and handle failures gracefully?
- How do you enforce quotas and prevent abuse?
- How do you observe a system you can't see inside?
- How do you keep costs under control when usage is unpredictable?

This project is my answer to those questions, applied to LLM-powered systems.

---

## Running Locally

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/MLops_Project.git
cd MLops_Project
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Configure
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Run
fastapi dev src/ai_platform/api/main.py

# Test
pytest
```

---

## Study Plan

This project follows a structured 6-month plan:

| Month | Focus | What Gets Built |
|---|---|---|
| 1 | Python Foundation | Config, HTTP client, logging, validation schemas |
| 2 | LLM Client + FastAPI | Anthropic wrapper, `/health` + `/chat` endpoints, security layer |
| 3 | Gateway + RAG | Multi-provider routing, fallback chains, embeddings, ChromaDB |
| 4 | Async + Observability | Async LLM calls, cost tracking, budget circuit breaker |
| 5 | Cloud Deployment | Cloud Run, Secret Manager, Cloud Monitoring, multi-tenancy |
| 6 | Specialization | Deep expertise + portfolio polish |

The full study plan PDF is included in this repo: [`AI_Infrastructure_Study_Plan.pdf`](./AI_Infrastructure_Study_Plan.pdf)

---

## Status

🟡 **In Progress** — Currently on Week 10 (Embeddings + Vector Database)

- [x] Month 1 — Python Foundation
- [x] Month 2 — LLM Client + FastAPI
- [x] Month 3 (partial) — Gateway Layer complete, RAG in progress
- [ ] Month 4 — Async + Observability
- [ ] Month 5 — Cloud Deployment
- [ ] Month 6 — Specialization

---

## License

MIT
