# uv dependency groups

This repository uses one `uv` project at the repository root:

- Python is fixed to `3.14` in `.python-version`.
- `pyproject.toml` contains shared dependency groups and one group per chapter.
- `uv.lock` is the single reproducible lockfile for every group.
- The root project is marked as `package = false` because the repository is a set of chapter scripts and notebooks, not an installable Python package.

## Install a chapter

Use the chapter group you want to work on:

```bash
uv sync --locked --only-group ch08
uv run --locked --only-group ch08 jupyter lab ch08/08-advanced_indexing.ipynb
```

For chapter 11 scripts:

```bash
uv sync --locked --only-group ch11
uv run --locked --only-group ch11 python ch11/main_01_01.py
```

The appendix group is named `ape`:

```bash
uv sync --locked --only-group ape
uv run --locked --only-group ape jupyter lab apE/local_llm.ipynb
```

## Environment layout

Dependency groups do not create separate virtual environments by themselves. By default, `uv sync` and `uv run` operate on the root `.venv`.

For an isolated chapter environment, set `UV_PROJECT_ENVIRONMENT`:

```bash
UV_PROJECT_ENVIRONMENT=.venv-ch08 uv sync --locked --only-group ch08
UV_PROJECT_ENVIRONMENT=.venv-ch08 uv run --locked --only-group ch08 python -c "import langchain_chroma"
```

The verification script uses this pattern automatically and creates one environment per group under `.venv-uv-groups/`.

## Verify all groups

```bash
python scripts/verify_uv_groups.py
```

Verify a subset:

```bash
python scripts/verify_uv_groups.py ch01 ch11 ape
```

The script performs two checks for each requested group:

1. `uv sync --locked --only-group <group>` succeeds in an isolated virtual environment.
2. The modules used by that chapter can be imported.

## Upgrade dependencies

To refresh all locked versions to the newest compatible releases for Python 3.14:

```bash
uv lock --upgrade
python scripts/verify_uv_groups.py
```

To upgrade only one group:

```bash
uv lock --upgrade-group ch11
python scripts/verify_uv_groups.py ch11
```

After verification, commit `pyproject.toml`, `uv.lock`, and any documentation or script changes together.
