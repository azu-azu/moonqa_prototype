# qa_pdf Prototype 🌙

This is a prototype QA system built with LangChain, designed to answer questions from a PDF document about the moon.
It uses vector search (FAISS) and OpenAI's language model to provide accurate, context-based answers.

---

## 🌌 Project Overview

- **Purpose**: Convert internal PDFs into a searchable vector database and enable natural language Q&A
- **Supported Input**: Any `.pdf` file placed inside the `data/` directory
- **Architecture**:
  - Text splitting via `RecursiveCharacterTextSplitter`
  - Embedding with `OpenAIEmbeddings`
  - Vector store: `FAISS`
  - LLM: `ChatOpenAI` (GPT-3.5-turbo or GPT-4)
  - Output: JSONL log (`logs/qa_log.jsonl`) and optional CLI output
  - Responses are generated in a soft Kansai dialect with line breaks at periods

---

## 🗂 Directory Structure

```
qa_pdf/
├── app/                       # Core logic
│   ├── qa.py                  # Answer generation logic
│   ├── config.py              # Path handling
│   ├── ingest.py              # CLI entry point｜PDF to chunk → embed → FAISS
│   ├── settings.py            # Constants like model name and thresholds
│   └── ...
├── data/                      # PDF input folder
│   ├── about_moon.pdf
│   ├── about_sun.pdf
│   └── ...
├── index/faiss_index/         # Vector DB (auto-generated)
│   ├── index.faiss
│   └── index.pkl
├── logs/
│   └── qa_log.jsonl           # Log of question/answer pairs
├── scripts/
│   ├── build_vectorstore.py   # 📌 Must re-run when PDFs are added/changed
│   ├── manual_run.py
│   └── multi_run.py
├── tests/                     # QA behavior inspection and test tools
│   ├── manual_vector_check.py     # Detailed chunk/source check (target_pdf support)
│   ├── manual_embedding_check.py  # Embedding/chunk inspection
│   ├── manual_qa_run_log.py       # Quick output test with log
│   └── test_qa_search.py          # pytest-compatible test
│
├── README.md
├── .gitignore
└── pyproject.toml
```
- `scripts/` directory contains both production and testing scripts.
  See [scripts/README.md](scripts/README.md) for full details.

---

## 🚀 Setup & Usage

1. **Install dependencies** with Poetry:

   ```bash
   poetry install
   ```

2. **Set your OpenAI API key and model** in `.env`:

   ```env
   OPENAI_API_KEY=your-api-key
   OPENAI_MODEL=gpt-3.5-turbo
   ```

3. **Add your PDFs** to the `data/` folder.

4. **Build the vector index** (must re-run every time you add/remove PDFs):

   ```bash
   poetry run python scripts/build_vectorstore.py
   ```

5. **Run the QA system via CLI**:

   ```bash
   poetry run python main.py
   ```

   → This will prompt you for a question and return an answer.

---

## 📒 Output

Each question/answer pair is appended to `logs/qa_log.md` in the following Markdown format:

```markdown
## 💬 Question
月には水がありますか？

## 📖 Answer
月の表面には「海」と呼ばれる平らな地形がありますが、実際には水は存在しません。
---
```

---

## 🔧 Configuration Notes

- OpenAI API key and model settings should be defined in your `.env` file:
- Thresholds and app-specific parameters are set in `app/settings.py`.
For example, `SCORE_THRESHOLD` controls the similarity score cutoff used during retrieval (range: 0.0–1.0).

---

## 📌 Notes

- When using `target_pdf`, only the matching PDF is searched by partial filename match
- Kansai dialect output is line-broken at periods (`。`) but not at commas (`、`)
- `logs/qa_log.jsonl` contains structured logs of questions and answers
- To check which vector chunks were used, run:

   ```bash
   poetry run python tests/manual_vector_check.py
   ```

---

## 🧪 Test Utilities

- `manual_vector_check.py` → Verify chunk content and source per question
- `manual_qa_run_log.py` → Basic CLI run + JSONL log
- `manual_embedding_check.py` → Inspect chunk count, embedding shape
- `test_qa_search.py` → Pytest-ready check

---

## 📘 License

This repository is currently private and intended for internal testing only.
