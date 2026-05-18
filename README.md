# Building LLM Applications

A fork of the companion code for the book **AI Applications with LangChain**,
restructured as a single **uv** monorepo so every chapter shares one
reproducible lockfile.

## Repository layout

```
.
├── apE/                # Appendix E
├── ch01/ … ch11/       # One folder per chapter
├── docs/uv.md          # Detailed uv workflow
├── scripts/
│   └── verify_uv_groups.py
├── pyproject.toml      # Shared deps + per-chapter dependency groups
├── uv.lock             # Single reproducible lockfile for the whole repo
└── .python-version     # Pinned to 3.14
```

Each chapter folder contains its scripts / notebooks; **all dependencies live
at the repo root** in `pyproject.toml`.

## Why a uv monorepo

Original book layout shipped one `requirements.txt` per chapter. This fork
replaces them with a single `uv` project at the root:

* One Python version (`.python-version` -> 3.14) for every chapter.
* `pyproject.toml` declares **shared groups** (e.g. `langchain-base`,
  `web-search`, `rag`) and **one group per chapter** (`ch01` … `ch11`, `ape`)
  that compose those shared groups.
* A single `uv.lock` pins exact versions across all chapters; the pinned
  versions track current stable releases of `langchain` (1.3.x),
  `langchain-openai` (1.2.x), `langgraph` (1.2.x), etc.
* Per-chapter `requirements.txt` files have been removed. Treat
  `pyproject.toml` + `uv.lock` as the source of truth.
* The root project is marked `package = false` because this is a collection
  of chapter scripts and notebooks, not an installable Python package.

## Prerequisites

* `uv` (>= 0.5): <https://docs.astral.sh/uv/getting-started/installation/>
* Python 3.14 (uv will provision it automatically based on `.python-version`)
* An `OPENAI_API_KEY` for chapters that call the OpenAI API
* Some chapters need extra services (e.g. SQLite for the ch11 hotel demo) —
  see the chapter's own README when present.

## Quick start

```bash
# Clone and enter the repo
git clone <repo-url> building-llm-applications
cd building-llm-applications

# Install dependencies for one chapter (creates ./.venv)
uv sync --locked --only-group ch04

# Run a chapter script
uv run --locked --only-group ch04 python ch04/chain_try_1_2.py

# Or launch Jupyter for a notebook-based chapter
uv sync --locked --only-group ch08
uv run --locked --only-group ch08 jupyter lab ch08/08-advanced_indexing.ipynb
```

Set `OPENAI_API_KEY` (and any other chapter-specific keys) either in your
shell or in a chapter-local `.env` — see `chXX/.env_example` where provided.

## Working with dependency groups

* Look up which group you need in `pyproject.toml` under
  `[dependency-groups]`. Chapter groups like `ch04` are composed from shared
  groups via `{ include-group = "..." }`.
* By default `uv sync` / `uv run` reuse the root `.venv`. To isolate one
  chapter into its own virtualenv:

```bash
UV_PROJECT_ENVIRONMENT=.venv-ch08 uv sync --locked --only-group ch08
UV_PROJECT_ENVIRONMENT=.venv-ch08 uv run --locked --only-group ch08 \
    jupyter lab ch08/08-advanced_indexing.ipynb
```

## Upgrade dependencies

```bash
# Refresh every group to the newest releases compatible with Python 3.14
uv lock --upgrade
python scripts/verify_uv_groups.py

# Or upgrade only a single chapter group
uv lock --upgrade-group ch11
python scripts/verify_uv_groups.py ch11
```

After verification, commit `pyproject.toml`, `uv.lock`, and any code or doc
changes together.

## Verify all groups

`scripts/verify_uv_groups.py` provisions an isolated virtualenv per group
under `.venv-uv-groups/`, runs `uv sync --locked --only-group <group>`, and
imports the modules each chapter relies on.

```bash
python scripts/verify_uv_groups.py            # all groups
python scripts/verify_uv_groups.py ch01 ch11  # a subset
```

## Further reading

* [`docs/uv.md`](docs/uv.md) — extended uv workflow, including environment
  layout and per-group verification details.
* Chapter-specific READMEs (where present) document additional setup steps,
  e.g. [`ch11/README.md`](ch11/README.md) for the LangGraph travel assistant.
