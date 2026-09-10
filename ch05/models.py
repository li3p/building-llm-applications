from langchain_openai import ChatOpenAI
from typing import List, Dict, Any, TypedDict, Optional, NotRequired
from dotenv import load_dotenv, find_dotenv
import os

# 自动向上查找到项目根目录下的 .env 文件
load_dotenv(find_dotenv(usecwd=True))

def get_llm():
    """
    动态获取 LLM 实例，确保即使在 LangGraph Server 等子进程/热重载环境中，
    也能实时获取最新的环境变量（如用户私有 VLLM 的 BASE_URL 与 MODEL）。
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    kwargs = {
        "model": model,
        "model_name": model,
    }
    if api_key:
        kwargs["api_key"] = api_key
        kwargs["openai_api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
        kwargs["openai_api_base"] = base_url

    return ChatOpenAI(**kwargs)

# Define typed dictionaries for state handling
class AssistantInfo(TypedDict):
    assistant_type: str
    assistant_instructions: str
    user_question: str

class SearchQuery(TypedDict):
    search_query: str
    user_question: str

class SearchResult(TypedDict):
    result_url: str
    search_query: str
    user_question: str
    is_fallback: Optional[bool]

class SearchSummary(TypedDict):
    summary: str
    result_url: str
    user_question: str
    is_fallback: Optional[bool]

class ResearchReport(TypedDict):
    report: str

# Graph state
class ResearchState(TypedDict):
    user_question: str
    target_language: NotRequired[Optional[str]]  # 目标输出语言，如 "Chinese"、"English" 等，可选
    assistant_info: NotRequired[Optional[AssistantInfo]]
    search_queries: NotRequired[Optional[List[SearchQuery]]]
    search_results: NotRequired[Optional[List[SearchResult]]]
    search_summaries: NotRequired[Optional[List[SearchSummary]]]
    research_summary: NotRequired[Optional[str]]
    final_report: NotRequired[Optional[str]]
    used_fallback_search: NotRequired[Optional[bool]]
    relevance_evaluation: NotRequired[Optional[Dict[str, Any]]]
    should_regenerate_queries: NotRequired[Optional[bool]]
    iteration_count: NotRequired[Optional[int]]
