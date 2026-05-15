import os
from pathlib import Path

from dotenv import dotenv_values
from langchain_openai import ChatOpenAI


ROOT_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
CHAPTER_ENV_FILE = Path(__file__).with_name(".env")


def _load_config() -> dict[str, str]:
    config: dict[str, str] = {}
    for env_file in (ROOT_ENV_FILE, CHAPTER_ENV_FILE):
        config.update(
            {key: value for key, value in dotenv_values(env_file).items() if value}
        )
    config.update(os.environ)
    return config


CONFIG = _load_config()


def _required_env(name: str) -> str:
    value = CONFIG.get(name)
    if not value:
        raise RuntimeError(
            f"Missing {name}. Set it in {ROOT_ENV_FILE} or create {CHAPTER_ENV_FILE} from ch04/.env_example."
        )
    return value


def get_llm():
    return ChatOpenAI(
        openai_api_key=_required_env("OPENAI_API_KEY"),
        model=CONFIG.get("OPENAI_MODEL", "gpt-5-nano"),
        temperature=float(CONFIG.get("OPENAI_TEMPERATURE", "1")),
    )
