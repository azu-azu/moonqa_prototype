# tests/manual_vector_check.py

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.qa import get_answer, load_vectorstore

# 質問内容（テスト切り替え用：必要に応じてコメントアウトで変更）
# QUESTION = "このPDFは何について書かれていますか？"
# QUESTION = "月って何？"
# QUESTION = "月の特徴は？"
# QUESTION = "月って、どうやってできたの？"
# QUESTION = "地球とはどんな関係にあるの？"
# QUESTION = "なんか面白いこと教えて。"
QUESTION = "太陽はどうやって光ってるの？"

def manual_vector_check_all():
    """
    すべてのPDFを対象に検索テストする関数。
    チャンク内容・スコア・参照元を含めて出力する。
    """
    vectorstore = load_vectorstore()
    answer, docs_and_scores = get_answer(QUESTION, vectorstore)

    print("💬 質問:", QUESTION)
    print("📁 検索対象: すべてのPDF")
    print("💡 回答:\n", answer)
    print_chunk_info_markdown(docs_and_scores)

def manual_vector_check_with_filter():
    """
    特定のPDF（target_pdf）のみに絞って検索するテスト関数。
    """
    vectorstore = load_vectorstore()
    target_pdf = "about_sun.pdf"

    answer, docs_and_scores = get_answer(QUESTION, vectorstore, target_pdf=target_pdf)

    print("💬 質問:", QUESTION)
    print("📁 検索対象:", target_pdf)
    print("💡 回答:\n", answer)
    print_chunk_info_markdown(docs_and_scores)

def print_chunk_info_markdown(docs_and_scores):
    """
    使用されたチャンク情報を Markdown形式で整形・出力する。
    - 各チャンクのスコア・参照元・先頭500文字を表示。
    """
    print("\n## 🔍 使用チャンク情報\n")
    for i, (doc, score) in enumerate(docs_and_scores):
        source = doc.metadata.get("source", "unknown")
        print(f"### Chunk {i+1}")
        print(f"- **Score**: {score:.4f}")
        print(f"- **Source**: {source}")
        print("```\n" + doc.page_content.strip()[:500] + "\n```")
        print()

def validate_source_format(docs_and_scores):
    """
    チャンクの source メタ情報が適切な形式かを検証する関数。

    - ファイル名に加えてページ番号 (p.N) が含まれているかを確認する。
    - logs/から直接検証したいときなど、手動で呼び出して使う。
    """
    print("\n✅ sourceフォーマット検証結果:")

    for i, (doc, score) in enumerate(docs_and_scores):
        source = doc.metadata.get("source", "❌ 不明")
        print(f"--- Doc {i+1} ---")
        print(f"📁 source: {source}", end=" ")

        # ✅ sourceがちゃんと (p.N) を含んでるか”を視認しやすくする
        if "(p." in source:
            print("✅ page info OK")
        else:
            print("⚠️ page info MISSING")

        print("📝 content preview:")
        print(doc.page_content.strip()[:300])
        print()

if __name__ == "__main__":
    # ✅ 実行したいテストを有効化（他はコメントアウト）
    manual_vector_check_with_filter()
    # manual_vector_check_all()
    # validate_source_format(...) ← docs_and_scores を引数に渡す必要あり（手動用）
