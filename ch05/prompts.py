from langchain_core.prompts import PromptTemplate

# web search and summarization prompts adapted from: https://github.com/langchain-ai/langchain/blob/master/templates/research-assistant/research_assistant/search/web.py 

# ASSISTANT SELECTION
ASSISTANT_SELECTION_INSTRUCTIONS = """
You are skilled at assigning a research question to the correct research assistant. 
There are various research assistants available, each specialized in an area of expertise. 
Each assistant is identified by a specific type. Each assistant has specific instructions to undertake the research.

How to select the correct assistant: you must select the relevant assistant depending on the topic of the question, which should match the area of expertise of the assistant.

------
Here are some examples on how to return the correct assistant information, depending on the question asked.

Examples:
Question: "Should I invest in Apple stocks?"
Response: 
{{
    "assistant_type": "Financial analyst assistant",
    "assistant_instructions": "You are a seasoned finance analyst AI assistant. Your primary goal is to compose comprehensive, astute, impartial, and methodically arranged financial reports based on provided data and trends.",
    "user_question": {user_question}
}}
Question: "what are the most interesting sites in Tel Aviv?"
Response: 
{{
    "assistant_type": "Tour guide assistant",
    "assistant_instructions": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights.",
    "user_question": "{user_question}"
}}

Question: "Is Messi a good soccer player?"
Response: 
{{
    "assistant_type": "Sport expert assistant",
    "assistant_instructions": "You are an experienced AI sport assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured sport reports on given sport personalities, or sport events, including factual details, statistics and insights.",
    "user_question": "{user_question}"
}}

------
Now that you have understood all the above, select the correct research assistant for the following question.
Question: {user_question}
Response:

""" 

ASSISTANT_SELECTION_PROMPT_TEMPLATE = PromptTemplate.from_template( 
    template=ASSISTANT_SELECTION_INSTRUCTIONS
)

# WEB SEARCH
WEB_SEARCH_INSTRUCTIONS = """
{assistant_instructions}

Write {num_search_queries} web search queries to gather as much information as possible 
on the following question: {user_question}. Your objective is to write a report based on the information you find.
If the question is in Chinese, generate search queries in Chinese (or a suitable combination of Chinese and professional domain terminology) to find the most relevant information.
You must respond with a list of queries such as query1, query2, query3 in the following format: 
[
    {{"search_query": "query1", "user_question": "{user_question}" }},
    {{"search_query": "query2", "user_question": "{user_question}" }},
    {{"search_query": "query3", "user_question": "{user_question}" }}
]
"""

WEB_SEARCH_PROMPT_TEMPLATE = PromptTemplate.from_template(
    template=WEB_SEARCH_INSTRUCTIONS
)

# INDIVIDUAL SEARCH SUMMARY
SUMMARY_INSTRUCTIONS = """
Read the following text:
Text: {search_result_text} 

-----------

Using the above text, answer in short the following question in Chinese (简体中文).
Question: {search_query}
 
-----------
If you cannot answer the question above using the text provided above, then just summarize the text in Chinese. 
Include all factual information, numbers, stats etc if available.
"""

SUMMARY_PROMPT_TEMPLATE = PromptTemplate.from_template(
    template=SUMMARY_INSTRUCTIONS
)

# RESEARCH REPORT
# Research Report prompts adapted from https://github.com/assafelovic/gpt-researcher/blob/master/gpt_researcher/master/prompts.py
RESEARCH_REPORT_INSTRUCTIONS = """
You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text.

Information: 
--------
{research_summary}
--------

Using the above information, answer the following question or topic: "{user_question}" in a detailed report.

CRITICAL LANGUAGE & FORMAT REQUIREMENTS:
- You MUST write the entire report in fluent, professional, and well-structured {target_language}, regardless of whether the source material is in English or other languages.
- The report should focus on answering the question directly, with clear structure, in-depth analysis, logical reasoning, and concrete facts/figures if available.
- Length requirement: Aim for a comprehensive and thorough report (at least 1,500 words/characters).
- Use Markdown syntax with clear headings (#, ##, ###), bullet points, and emphasis where appropriate.
- You MUST formulate your own concrete, rigorous, and valid analytical conclusions based on the provided information. Do NOT fall back on vague or empty generalities.
- List all unique source URLs at the end of the report under a References / 参考来源 section.
- Please do your best, this is very important to my career."""

RESEARCH_REPORT_PROMPT_TEMPLATE = PromptTemplate.from_template(
    template=RESEARCH_REPORT_INSTRUCTIONS
)
