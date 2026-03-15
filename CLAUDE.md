# CLAUDE.md — AI Content Engine

This file documents the codebase structure, development workflows, and conventions for AI assistants working in this repository.

---

## Project Overview

**AI Content Engine** is a Python-based proof-of-concept (PoC) application that generates SEO-optimized articles using Mistral AI (via LangChain), provides real-time SEO scoring, and stores generated content in a local SQLite database. The current UI is built with Streamlit. A live demo is available at https://aicontentengine.streamlit.app/.

The roadmap calls for a Phase 2 migration to a **Next.js frontend + FastAPI backend + PostgreSQL** stack. See `Docs.md` for details.

---

## Repository Structure

```
AI_content_engine/
├── app.py                   # Streamlit entry point
├── requirements.txt         # Python dependencies
├── verify_backend.py        # Assertion-based backend tests
├── verify_backend_file.py   # File-based verification (CI-friendly)
├── README.md                # Project overview and setup guide
├── Docs.md                  # Architecture & two-phase roadmap
├── TDD.md                   # Product & system requirements (PRD/SRD)
└── src/
    ├── __init__.py          # Package init (empty)
    ├── content_gen.py       # LLM article generation (Mistral via LangChain)
    ├── seo.py               # Rule-based SEO analysis and scoring
    ├── plagiarism.py        # Plagiarism check (currently mocked)
    └── db.py                # SQLite database management
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI (PoC) | Streamlit |
| LLM Orchestration | LangChain + `langchain-mistralai` |
| LLM Model | `mistral-large-latest` |
| Database | SQLite3 (`data/content.db`) |
| Config | python-dotenv (`.env` file) |

---

## Environment Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables** — create a `.env` file in the project root:
   ```
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```
   The app also accepts the key at runtime via the Streamlit sidebar.

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Run backend verification**
   ```bash
   python verify_backend.py          # Assertion-based (prints PASS/FAIL per test)
   python verify_backend_file.py     # Writes result to verification_result.txt
   ```

The SQLite database (`data/content.db`) and the `data/` directory are created automatically on first run.

---

## Module Conventions

### `src/content_gen.py`
- Single public function: `generate_article(topic: str, keywords: list[str]) -> str`
- Uses `ChatPromptTemplate` + `StrOutputParser` from LangChain
- Model temperature: `0.7`
- Raises a descriptive `ValueError` for missing or invalid API keys — callers should catch this
- Instructs the model to produce Markdown-formatted, legally appropriate content

### `src/seo.py`
- Single public function: `analyze_seo(text: str, keywords: list[str]) -> dict`
- Return shape: `{"score": int, "suggestions": list[str]}`
- Scoring starts at 100 and applies deductions:
  - `-20` if word count < 300
  - `-10` per missing keyword
  - `-5` if any keyword appears more than 5 times (keyword stuffing)
  - `-10` if average sentence length > 20 words
- Score is clamped to a minimum of `0`
- Keep this module pure (no I/O, no API calls)

### `src/plagiarism.py`
- Single public function: `check_plagiarism(text: str) -> dict`
- Return shape: `{"uniqueness_score": int, "is_plagiarized": bool, "details": str}`
- **Currently a mock** — returns a random uniqueness score between 85–100%
- When integrating a real API (e.g., Copyscape, Turnitin), replace the mock body without changing the function signature or return shape

### `src/db.py`
- Three public functions:
  - `init_db()` — creates the `articles` table if it does not exist
  - `save_article(topic, keywords, content, seo_score)` — inserts a record; `keywords` is stored as a comma-joined string
  - `get_articles()` — returns all rows ordered by `created_at DESC`
- Database path: `data/content.db` (relative to the project root)
- Do not change the table schema without updating all call sites in `app.py` and both verification scripts

---

## app.py Conventions

- `init_db()` is called at module load time to ensure the database exists before any UI renders
- API key is read from `MISTRAL_API_KEY` env var; if absent, the sidebar prompts the user
- Layout: two-column — left column for input (topic, keywords), right column for generated content and analysis
- All state (generated content, SEO results, plagiarism results) is managed via `st.session_state`

---

## Testing

There is no formal test framework (pytest, unittest) yet. Verification is done via two standalone scripts:

| Script | Purpose |
|---|---|
| `verify_backend.py` | Runs `test_seo()`, `test_plagiarism()`, `test_db()`, `test_content_gen_mock()` with assertions; prints per-test results |
| `verify_backend_file.py` | Simplified check; writes `PASS` or `FAIL: <error>` to `verification_result.txt` |

**When adding new modules**, add corresponding test functions to `verify_backend.py` following the existing pattern: a function named `test_<module>()` that uses `assert` statements and is called in the `if __name__ == "__main__"` block.

---

## Git Workflow

- **Feature branches** follow the pattern `claude/<short-description>-<session-id>`
- Commit messages use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- Push with: `git push -u origin <branch-name>`
- Do **not** push directly to `master` or `main`

---

## Key Constraints & Gotchas

- **Plagiarism module is mocked.** Do not treat `uniqueness_score` as real data until a real API is wired in.
- **Single-user PoC.** There is no authentication, session isolation, or rate limiting. Do not implement multi-user patterns against the current Streamlit + SQLite stack without first migrating to the Phase 2 architecture.
- **No Docker / CI/CD yet.** Do not assume a containerized environment. All paths are relative to the project root.
- **Database migrations are manual.** There is no migration framework. If the schema changes, `data/content.db` must be deleted and re-initialized.
- **Streamlit is temporary.** Avoid building complex UI logic into `app.py` that cannot be easily ported to a FastAPI + Next.js stack.
- **`data/` directory is not tracked by git.** It is created at runtime. Do not commit `data/content.db`.

---

## Planned Phase 2 Architecture

| Component | Technology |
|---|---|
| Frontend | Next.js |
| Backend API | FastAPI (Python) |
| Database | PostgreSQL |
| Auth | TBD |

When working toward Phase 2, new API endpoints should follow RESTful conventions and be placed in a new `api/` directory. The `src/` modules (`content_gen`, `seo`, `plagiarism`, `db`) are designed to be imported directly by a FastAPI app with minimal changes.

---

## Useful References

- `Docs.md` — architecture diagrams and phased roadmap
- `TDD.md` — full PRD and SRD including performance targets (< 5 s per article generation)
- `README.md` — quick setup guide
