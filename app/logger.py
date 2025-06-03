# app/logger.py

import os
import json
from datetime import datetime
import uuid
from filelock import FileLock  # 排他制御を導入

LOG_FILE_PATH = "logs/qa_log.jsonl"
LOG_LOCK_PATH = LOG_FILE_PATH + ".lock"

def ensure_log_dir_exists():
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def generate_query_id():
    return str(uuid.uuid4())

def append_qa_log(entry):
    with FileLock(LOG_LOCK_PATH):
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")

def build_log_entry(question, answer, results, status="success", intent=None, query_id=None):
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query_id": query_id or generate_query_id(),
        "question": question,
        "answer": answer,
        "status": status,  # e.g., "success", "notfound"
        "intent": intent,  # optional: "pdf_question", "chitchat", etc.
        "results": results
    }
