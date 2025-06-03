# scripts/manual_run.py

# ✅ テスト用スクリプト
# 単発の質問に対して、QAとチャンク出力を実行する簡易チェックツール
# QAロジックの検証や、埋め込み結果の妥当性チェックに使用

from app.qa import load_vectorstore, get_answer
from tests.manual_vector_check import print_chunk_info_markdown

# --- 質問をここに書く ---
question = "月って、どうやってできたの？"

# --- ベクトルストア読み込み ---
vectorstore = load_vectorstore()

# --- 回答実行 ---
answer, docs_and_scores = get_answer(question, vectorstore)

# --- 回答表示 ---
print("\n💡 回答:")
print(answer)

# --- 使用チャンク情報をMarkdown形式で表示 ---
print_chunk_info_markdown(docs_and_scores)
