# UK Travel Assistant – LangGraph (ToolNode pattern)

This project is an example of the **"Add tools"** LangGraph tutorial [§4 Define the graph](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#4-define-the-graph) applied to a travel assistant.

The assistant can answer questions about WikiVoyage pages for:

* Cornwall
* North Cornwall
* South Cornwall
* West Cornwall

It relies on a **single tool** (`search_travel_info`) and the standard pre-built components `tools_condition` + custom `CustomToolNode`.

---

## Setup

Dependencies are managed with `uv` at the repository root. See
[`docs/uv.md`](../docs/uv.md) for the full workflow.

```bash
# 1 · Install the ch11 dependency group
uv sync --locked --only-group ch11

# 2 · OpenAI key (session-only)
export OPENAI_API_KEY="sk-..."

# 3 · Run
uv run --locked --only-group ch11 python ch11/main.py
```

---

### Internals

* **Vector store:** Pages fetched with `AsyncHtmlLoader`, chunked and embedded with `OpenAIEmbeddings`, stored in **Chroma**.
* **Tool:** `search_travel_info` performs similarity search and returns top chunks.
* **LangGraph:**
  * `chatbot` node -> LLM (may emit tool_calls).
  * `tools` node -> `CustomToolNode` executes those calls.
  * `tools_condition` routes between them.
* **Loop:** After each tool call, control returns to the LLM until a final answer is produced. 

## Setting up the SQLite Database for Hotel Booking

To use the hotel booking features, you need to create and populate a SQLite database with hotel and room offer data.

### 1. Install SQLite (if not already installed)
- On most systems, you can install SQLite via your package manager, or download it from https://www.sqlite.org/download.html

### 2. Create the Database and Tables
- Open a terminal and navigate to the `hotel_db` directory:
  
  ```sh
  cd hotel_db
  ```

- Run the following command to create the database and populate it with sample data:
  
  ```sh
  sqlite3 cornwall_hotels.db < cornwall_hotels_schema.sql
  ```

  This will create a file named `cornwall_hotels.db` in the `hotel_db` directory, containing the required tables and data.

### 3. Verify the Database (optional)
- You can open the SQLite shell to inspect the database:
  
  ```sh
  sqlite3 cornwall_hotels.db
  sqlite> .tables
  sqlite> SELECT * FROM hotels;
  sqlite> SELECT * FROM hotel_room_offers;
  ```

Now your database is ready for use with the application! 