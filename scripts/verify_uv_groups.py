from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_ROOT = ROOT / ".venv-uv-groups"

GROUP_IMPORTS: dict[str, tuple[str, ...]] = {
    "ape": ("notebook", "openai", "langchain_openai"),
    "ch01": ("notebook", "langchain", "langchain_openai"),
    "ch02": ("notebook", "openai", "langchain", "langchain_openai"),
    "ch03": (
        "docx2txt",
        "langchain",
        "langchain_community",
        "langchain_openai",
        "langchain_text_splitters",
        "notebook",
        "pypdf",
        "tiktoken",
        "wikipedia",
    ),
    "ch04": (
        "bs4",
        "ddgs",
        "dotenv",
        "duckduckgo_search",
        "langchain",
        "langchain_community",
        "langchain_openai",
        "requests",
    ),
    "ch05": (
        "bs4",
        "ddgs",
        "dotenv",
        "duckduckgo_search",
        "langchain",
        "langchain_community",
        "langchain_openai",
        "langgraph",
        "requests",
    ),
    "ch06": ("chromadb", "notebook", "openai"),
    "ch07": (
        "chromadb",
        "docx2txt",
        "langchain",
        "langchain_chroma",
        "langchain_community",
        "langchain_openai",
        "langchain_text_splitters",
        "notebook",
        "openai",
        "pypdf",
        "wikipedia",
    ),
    "ch08": (
        "chromadb",
        "html2text",
        "langchain",
        "langchain_chroma",
        "langchain_classic",
        "langchain_community",
        "langchain_openai",
        "langchain_text_splitters",
        "lark",
        "lxml",
        "notebook",
    ),
    "ch09": (
        "chromadb",
        "html2text",
        "langchain",
        "langchain_chroma",
        "langchain_classic",
        "langchain_community",
        "langchain_openai",
        "langchain_text_splitters",
        "lark",
        "lxml",
        "notebook",
    ),
    "ch10": (
        "chromadb",
        "html2text",
        "langchain",
        "langchain_chroma",
        "langchain_classic",
        "langchain_community",
        "langchain_openai",
        "langchain_text_splitters",
        "lark",
        "lxml",
        "notebook",
    ),
    "ch11": (
        "aiohttp",
        "bs4",
        "chromadb",
        "dotenv",
        "fastmcp",
        "html2text",
        "langchain",
        "langchain_chroma",
        "langchain_classic",
        "langchain_community",
        "langchain_mcp_adapters",
        "langchain_openai",
        "langchain_text_splitters",
        "langgraph",
        "langgraph_supervisor",
        "lxml",
        "tiktoken",
    ),
}


def run(command: list[str], *, env: dict[str, str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def python_executable(environment: Path) -> Path:
    if sys.platform == "win32":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def verify_group(group: str, env_root: Path, recreate: bool) -> None:
    environment = env_root / group
    if recreate and environment.exists():
        shutil.rmtree(environment)

    env = os.environ.copy()
    env["UV_PROJECT_ENVIRONMENT"] = str(environment)

    run(["uv", "sync", "--locked", "--only-group", group], env=env)

    imports = "; ".join(f"import {module}" for module in GROUP_IMPORTS[group])
    command = [
        str(python_executable(environment)),
        "-c",
        f"{imports}; print('ok: {group}')",
    ]
    run(command, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync each uv dependency group in an isolated environment and import its direct modules."
    )
    parser.add_argument(
        "groups",
        nargs="*",
        choices=sorted(GROUP_IMPORTS),
        help="Groups to verify. Defaults to every chapter group plus apE.",
    )
    parser.add_argument(
        "--env-root",
        type=Path,
        default=DEFAULT_ENV_ROOT,
        help="Directory used for per-group virtual environments.",
    )
    parser.add_argument(
        "--reuse",
        action="store_true",
        help="Reuse existing per-group virtual environments instead of recreating them.",
    )
    args = parser.parse_args()

    groups = args.groups or list(GROUP_IMPORTS)
    for group in groups:
        verify_group(group, args.env_root, recreate=not args.reuse)


if __name__ == "__main__":
    main()
