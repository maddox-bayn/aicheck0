# aicheck0 — Automated AI Engineering Checkpoint System

Welcome to **`aicheck0`** (`github.com/maddox-bayn/aicheck0`) — an industry-standard, self-paced **20-Checkpoint, 200-Exercise** AI Engineering evaluation harness in Python.

```text
[Level 1: Minimal Python] ──> [Level 2: CLI Chatbot] ──> [Level 3: RAG Engine] ──> [Level 4: Multi-Tool Agent] ──> [Level 5: Production & Eval]
```

---

## Using This Repository as a Template

1. Click the **"Use this template"** button on GitHub (`github.com/maddox-bayn/aicheck0` -> **Create a new repository**).
2. Clone your newly created repository locally:
   ```bash
   git clone https://github.com/<your-username>/aicheck0.git
   cd aicheck0
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows PowerShell: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install -e .
   ```

---

## Configuring Your Free AgentRouter.org API Key

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and set your **AgentRouter.org** API key and model:
   ```ini
   AGENTROUTER_API_KEY=ar-xxxxxxxxxxxxxxxxxxxxxxxx
   AGENTROUTER_BASE_URL=https://api.agentrouter.org/v1
   AI_MODEL=deepseek-chat
   AI_TIMEOUT=30
   ```
3. Test live connectivity anytime with:
   ```bash
   python live_agentrouter_check.py
   ```
*(Note: All 200 automated unit tests in `pytest` use deterministic local mocks/fixtures so they run offline in milliseconds and pass in GitHub Actions without exposing your secret API key!)*

---

## Running the Checkpoint Grader (`aicheck_cli.py`)

* **Sequential Progression Mode (Recommended):**
  Runs checkpoints in strict order (`cp01` -> `cp20`) and stops at the first incomplete checkpoint:
  ```bash
  python aicheck_cli.py next
  ```
* **Grade a Single Checkpoint (`cp01` through `cp20`):**
  ```bash
  python aicheck_cli.py cp01
  python aicheck_cli.py cp05 -x
  ```
* **Grade an Entire Level (`level1` through `level5` or `all`):**
  ```bash
  python aicheck_cli.py level1
  python aicheck_cli.py all
  ```

---

## Syllabus Overview (20 Checkpoints / 200 Exercises)

| Level | Checkpoints | Core Focus |
| :--- | :--- | :--- |
| **Level 1: MVP Python** | `cp01` – `cp04` | Prompt formatting, message collections, control flow, `.env` & resilient JSON parsing |
| **Level 2: CLI Chatbot** | `cp05` – `cp08` | Raw HTTP/SSE, OpenAI/AgentRouter SDK, sliding window memory, resilient CLI chatbot |
| **Level 3: RAG Engine** | `cp09` – `cp12` | Document ingestion, AST/recursive chunking, embeddings/BM25/MMR, vector stores & RAG |
| **Level 4: AI Agents** | `cp13` – `cp16` | Pydantic schemas, safe tool dispatch, ReAct/state-graph loops, multi-agent orchestration |
| **Level 5: Production** | `cp17` – `cp20` | FastAPI SSE serving, guardrails & tracing, LLM-as-a-Judge evals, semantic caching |
