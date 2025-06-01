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

def validate_log_entry(path: str):
    """
    ログファイルの最後のエントリを読み取り、構造チェックを行う。
    必須キーがなければ ValueError を投げる。
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            raise ValueError("ログファイルが空です")

        last_line = lines[-1]
        try:
            data = json.loads(last_line)
        except json.JSONDecodeError as e:
            raise ValueError(f"ログがJSONとして不正です: {e}")

        required_keys = ["timestamp", "question", "answer", "results"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"ログに必要なキーがありません: {key}")

        if not isinstance(data["results"], list):
            raise ValueError("results フィールドが list ではありません")
