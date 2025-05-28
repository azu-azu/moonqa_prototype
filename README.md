# MoonQA Prototype 🌙

This is a prototype QA system built with LangChain, designed to answer questions from a PDF document about the moon.
It uses vector search (FAISS) and OpenAI's language model to provide accurate, context-based answers.

---

## 🌌 Project Overview

- **Purpose**: Test the ability to convert a PDF into vector data and query it using a natural language interface
- **PDF Input**: `data/about_moon.pdf`
- **Architecture**:
  - Text splitting with LangChain's `RecursiveCharacterTextSplitter`
  - Embedding via `OpenAIEmbeddings`
  - Vector store: FAISS
  - LLM: `ChatOpenAI (gpt-3.5-turbo)`
  - CLI-based query execution

---

## 🗂 Directory Structure

```
moonqa_prototype/
├── app/                 # Core logic (ingest, QA)
├── data/                # PDF source files
├── index/faiss_index/   # Vector index files (.faiss / .pkl)
├── logs/                # Markdown logs of questions and answers
├── .gitignore
├── README.md
├── pyproject.toml
└── main.py              # Entry point
```

---

## 🚀 How to Use

1. **Install dependencies** with Poetry:

   ```bash
   poetry install
   ```

2. **Set your OpenAI API key** in `.env`:

   ```
   OPENAI_API_KEY=your-key-here
   ```

3. **Run ingestion** to process the PDF:

   ```bash
   poetry run python app/ingest.py
   ```

4. **Ask a question via CLI**:

   ```bash
   poetry run python app/qa.py --question "月には水がありますか？"
   ```

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

## 📌 Notes

- This is a **prototype**, not production-ready
- LLM calls may incur OpenAI API costs
- `.env` is ignored and should not be committed

---

## 📘 License

This repository is currently private and intended for internal testing only.
