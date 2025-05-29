# scripts/manual_run.py

from app.qa import load_vectorstore, get_answer, print_chunk_info_markdown

# --- 質問をここに書く ---
question = "このPDFは何について書かれていますか？"

# --- ベクトルストア読み込み ---
vectorstore = load_vectorstore()

# --- 回答実行 ---
answer, docs_and_scores = get_answer(question, vectorstore)

# --- 回答表示 ---
print("\n💡 回答:")
print(answer)

# --- 使用チャンク情報をMarkdown形式で表示 ---
print_chunk_info_markdown(docs_and_scores)
