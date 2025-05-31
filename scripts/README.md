# scripts/ directory

This directory contains utility scripts for building and testing the vector-based QA system.

---

## 📁 Overview

| Script Name           | Purpose                                                | Type          |
|-----------------------|--------------------------------------------------------|---------------|
| `build_vectorstore.py`| Build FAISS index from PDF files                       | ✅ Production |
| `manual_run.py`       | Run a single QA query for testing and debugging        | 🔧 Test       |
| `multi_run.py`        | Run batch QA queries from a JSON file and log results  | 🔧 Test       |

---

## 🛠 Usage Notes

- **Run `build_vectorstore.py` every time** you add, delete, or update a PDF in `data/`.
- **Use `manual_run.py`** when you want to quickly test one question and view chunk-level details.
- **Use `multi_run.py`** when you want to run several QA tests in batch and save results to log files.

---

## 🔐 Tips

- All scripts are designed to be run via Poetry:

  ```bash
  poetry run python scripts/build_vectorstore.py
  poetry run python scripts/manual_run.py
  poetry run python scripts/multi_run.py
  ```

- Make sure your `.env` is set up correctly with the OpenAI API key.

