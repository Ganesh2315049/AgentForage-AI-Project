# Sentinel Agent

Sentinel Agent is a small, local security assistant built around the Ollama
`qwen3:8b` model. It accepts a security question, lets the model request
approved tools, validates every tool call, and returns an answer. The project
also includes a lightweight retrieval system for local Windows security notes,
input validation, structured logging, and a golden-set evaluation harness.

The project is intentionally local: questions are sent to the Ollama service
running on the developer's machine, and the retrieval tool reads only the
repository's local security notes.

## What the project does

The agent supports two tool-backed capabilities:

1. **Calculator** - performs addition, subtraction, multiplication, and
   division.
2. **Knowledge search** - finds relevant paragraphs in
   [`app/rag/security_notes.txt`](app/rag/security_notes.txt), which currently
   covers Windows Event IDs 4624 and 4625 and basic incident-response
   guidance.

Before the model is called, the input guardrail:

- requires a string;
- trims surrounding whitespace;
- rejects empty questions; and
- limits questions to 1,000 characters.

Tool calls are allow-listed by the registry and validated with strict Pydantic
schemas. Unknown tools, extra arguments, invalid operations, and division by
zero are rejected. Retrieved security text is explicitly marked as untrusted
evidence before it is sent back to the model.

## Request flow

```text
User question
    |
    v
validate_user_input()
    |
    v
Qwen via Ollama  <---- up to 5 agent/tool steps
    |                         |
    | final answer             | tool call
    |                         v
    |              allow-list lookup in tools.registry
    |                         |
    |              Pydantic argument validation
    |                         |
    |              calculator or knowledge_search
    |                         |
    +-------- tool result returned to Qwen
```

When the knowledge-search tool is used, the agent adds guidance telling the
model to treat retrieved text as data rather than instructions and not to
claim that an attack is confirmed without sufficient evidence. Each run is
logged to [`app/logs/sentinel_agent.log`](app/logs/sentinel_agent.log).

## Project layout

| Path | Purpose |
| --- | --- |
| [`app/agent.py`](app/agent.py) | Main tool-calling agent loop and safety guidance |
| [`app/main.py`](app/main.py) | Minimal one-shot chat entry point without tools |
| [`app/llm.py`](app/llm.py) | Ollama client wrapper and configured model name |
| [`app/schemas.py`](app/schemas.py) | Strict calculator input schema |
| [`app/tool_definitions.py`](app/tool_definitions.py) | Tool definitions sent to Qwen |
| [`app/tool_executor.py`](app/tool_executor.py) | Tool lookup, argument validation, and execution |
| [`app/guardrails/input_guardrail.py`](app/guardrails/input_guardrail.py) | User-input validation |
| [`app/tools/registry.py`](app/tools/registry.py) | Approved tool registry |
| [`app/tools/calculator.py`](app/tools/calculator.py) | Arithmetic implementation |
| [`app/tools/knowledge_search.py`](app/tools/knowledge_search.py) | Knowledge-search tool adapter |
| [`app/rag/retriever.py`](app/rag/retriever.py) | Paragraph-based keyword retrieval |
| [`app/rag/security_notes.txt`](app/rag/security_notes.txt) | Local security evidence |
| [`app/evals/evaluate_agent.py`](app/evals/evaluate_agent.py) | Runs golden-set cases through the live agent |
| [`app/evals/golden_set.json`](app/evals/golden_set.json) | Evaluation questions and expected criteria |
| [`app/evals/criteria_checker.py`](app/evals/criteria_checker.py) | Normalizes answers and checks required phrases |
| [`app/**/test_*.py`](app) | Unit tests, integration examples, and manual smoke scripts |

## Requirements

- Windows, or another platform able to run Python and Ollama
- Python 3.11 (the included virtual environment was created with Python 3.11.4)
- Ollama installed and running
- The `qwen3:8b` model available in Ollama
- Python packages: `ollama`, `pydantic`, and `pytest`

There is currently no `requirements.txt` or `pyproject.toml` in the repository,
so dependencies must be installed manually in the active environment.

## Setup on Windows

From the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install ollama pydantic pytest
ollama pull qwen3:8b
```

Start Ollama using the normal Ollama application or service. Verify that the
model is available before running the agent:

```powershell
ollama list
```

The source files use flat imports such as `from llm import ask_llm`, so run
application commands with [`app`](app) as the current directory.

## Running the agent

### Full tool-calling agent

```powershell
Set-Location app
python agent.py
```

The agent reads one question from standard input and prints tool results as
they are executed. It stops after five model/tool steps by default.

The reusable entry point is:

```python
from agent import run_agent

answer = run_agent("What does Windows Event ID 4625 mean?")
```

### Minimal direct chat

[`app/main.py`](app/main.py) calls the model directly and does not use the
agent loop, tools, input guardrail, or retrieval system:

```powershell
Set-Location app
python main.py
```

Use [`app/agent.py`](app/agent.py) when you want the project's security and
tool-execution behavior.

## Running tests

The repository contains both pytest tests and executable smoke/integration
examples. Some files whose names start with `test_` execute code during pytest
collection:

- [`app/test_qwen_tool_call.py`](app/test_qwen_tool_call.py) calls Ollama
  immediately and needs a running service and model.
- Several other `test_*.py` files print manual examples while being imported.

For the offline-compatible pytest suite, run from `app` and ignore the live
Ollama smoke script:

```powershell
Set-Location app
python -m pytest --ignore=test_qwen_tool_call.py
```

To run the Ollama tool-call smoke check explicitly:

```powershell
Set-Location app
python test_qwen_tool_call.py
```

The test suite covers input validation, tool allow-listing, strict argument
validation, calculator behavior, retrieval, logging, agent error handling, and
criteria checking.

## Running the evaluation harness

The evaluation harness runs every case in
[`app/evals/golden_set.json`](app/evals/golden_set.json) against the live Qwen
agent and checks the answer for required phrases:

```powershell
Set-Location app
python -m evals.evaluate_agent
```

The current golden set includes:

- Windows Event ID 4625 (failed logon)
- Windows Event ID 4624 (successful logon)
- calculator multiplication
- whether repeated failed logins alone prove an attack

Because these cases call the live model, results can vary with model behavior
and require Ollama to be available.

## Security and reliability notes

- **Tool boundary:** only tools in [`app/tools/registry.py`](app/tools/registry.py)
  can execute.
- **Schema boundary:** tool arguments are validated before execution and
  unknown fields are forbidden.
- **Prompt-injection handling:** retrieved notes are labeled untrusted data;
  retrieval is evidence, not an instruction source.
- **Input limit:** user questions are capped at 1,000 characters.
- **Agent loop limit:** the default maximum is five steps, preventing an
  unbounded tool-calling loop.
- **Evidence standard:** the bundled notes advise correlating accounts,
  sources, timestamps, and surrounding logs before confirming an incident.
- **Local retrieval limitation:** retrieval is simple case-insensitive
  whitespace/keyword overlap; it is not semantic search, stemming, or a
  production search index.
- **Model dependency:** the agent does not provide a fallback when Ollama is
  unavailable. The direct chat and evaluation paths therefore fail until the
  local service is running.

## Current development considerations

The project is a focused prototype rather than an installable package. If it
is expanded, useful next steps would be:

1. Add a dependency manifest and package configuration.
2. Separate live integration tests from pytest-collected unit tests.
3. Replace flat imports with a package layout or consistently configured
   module paths.
4. Add configurable model and Ollama endpoint settings.
5. Add retrieval tests for punctuation, ranking, missing notes, and
   case-insensitive queries.
