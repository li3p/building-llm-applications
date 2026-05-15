from llm_models import get_llm
from prompts import (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE, 
)

llm = get_llm()

assistant_instructions_chain = (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE | llm
)


if __name__ == "__main__":
    print(f"LLM: {llm.__class__.__name__}")
    print(f"model: {llm.model_name}")
    print(f"temperature: {llm.temperature}")
