import json
import os
from qa import question_answer_with_scores, append_markdown_log, append_json_log

# 質問ファイルの読み込み
with open("data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# スコアしきい値（必要に応じて調整）
score_threshold = 0.0

# 全件処理
for i, item in enumerate(questions):
    question = item.get("question", "").strip()
    if not question:
        continue

    print(f"\n[{i+1}/{len(questions)}] 質問: {question}")
    answer, docs_and_scores = question_answer_with_scores(question, score_threshold)
    append_markdown_log(question, answer, docs_and_scores)
    append_json_log(question, answer, docs_and_scores)
    print(f"💡 回答: {answer}")
