#  LLM Playground

> A personal collection of projects built while learning Large Language Models and AI engineering
<br>

---

## What is this?

This repository is my **learning journal in code** — a growing collection of small, focused projects built as I work through the fundamentals of LLM engineering. Each project explores a concept, tests an idea, or builds something fun with language models.

There's no pressure to be perfect here. This is a space for experimentation, breaking things, and figuring out how AI actually works under the hood — not just how to call an API.


---

## Projects

| # | Project | Description | Status |
|---|---------|-------------|--------|
| 01 | [**AI Web Scrapper**](./ai-web-scraper/) | Know summary of a website directly from terminal with using AI|  Completed |
| 02 | [**LLM vs LLM Chat**](./01-llm-chat/) | Two LLMs talk to each other in an autonomous loop |  In progress |

> More projects will be added as the learning journey continues.

---

## Tech Stack

Most projects in this repo draw from a shared toolkit:

**AI & Models**
- [Ollama](https://ollama.com) — run open-source models locally (Llama, Mistral, Gemma…)
- [OpenRouter](https://openrouter.ai) — access free open-source models via API
- [Anthropic Claude](https://www.anthropic.com) — frontier model for comparison & experimentation
- [OpenAI](https://openai.com) — GPT models for benchmarking

**Backend**
- Python 3.11+
- FastAPI — async API server
- WebSockets — real-time streaming

**Frontend**
- React
- Next.js
**Tooling**
- `uv` — Python package management
- `.env` files — API key management (never committed)

---

## Learning Goals

By building these projects, I'm working towards:

- [ ] Understanding how LLMs process and generate text
- [ ] Calling and comparing different model providers (OpenAI, Anthropic, local)
- [ ] Streaming responses and building real-time UIs
- [ ] Prompt engineering — system prompts, personas, chain-of-thought
- [ ] Building autonomous agents and multi-LLM workflows
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] Fine-tuning open-source models
- [ ] Evaluating and benchmarking model outputs

---

## Getting Started

Each project has its own setup instructions in its subdirectory. Most will need:

1. **Python 3.12+** and `pip` or `uv`
2. **Node.js 18+** for any frontend projects
3. **Ollama** installed locally for projects using local models → [ollama.com](https://ollama.com)
4. A free **OpenRouter** API key → [openrouter.ai](https://openrouter.ai)

Clone the repo and `cd` into any project folder to get started:

```bash
git clone https://github.com/dev-amanydv/mastering-llms.git
cd mastering-llms
```

---

## Notes on This Repo

- **This is a learning repo** — code quality will vary. Some things will be rough, experimental, or outright broken as I figure things out.
- **API keys are never committed** — all secrets live in `.env` files that are `.gitignore`'d.
- **Each project has its own `README.md`** with context, setup steps, and reflections.
- Projects are numbered sequentially so it's easy to follow the progression over time.


<p align="center">
  <sub>Built with curiosity · Powered by LLMs · Always a work in progress</sub>
</p>