# tests/log_utils.py

import os
import json
from datetime import datetime

def append_json_log(query, answer, docs_and_scores, log_path="logs/qa_log.jsonl"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": query,
        "answer": answer,
        "results": []
    }

    for doc, score in docs_and_scores:
        entry["results"].append({
            "score": float(score),
            "content": doc.page_content,
            "pdf_name": doc.metadata.get("pdf_name", "unknown"),
            "page": doc.metadata.get("page", -1),
            "source": doc.metadata.get("source", "unknown")
        })

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
