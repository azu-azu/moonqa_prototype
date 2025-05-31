# tests/manual_vector_check.py

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from app.qa import get_answer, load_vectorstore, print_chunk_info_markdown

# ✅ 共通の質問文を定数に
# QUESTION = "このPDFは何について書かれていますか？"
# QUESTION = "月って何？"
# QUESTION = "月の特徴は？"
# QUESTION = "月って、どうやってできたの？"
# QUESTION = "地球とはどんな関係にあるの？"
# QUESTION = "なんか面白いこと教えて。"
QUESTION = "太陽はどうやって光ってるの？"

def manual_vector_check_all():
    """
    全PDFを対象にした検索テスト
    """
    vectorstore = load_vectorstore()

    answer, docs_and_scores = get_answer(QUESTION, vectorstore)

    print("💬 質問:", QUESTION)
    print("📁 検索対象: すべてのPDF")
    print("💡 回答:\n", answer)
    print_chunk_info_markdown(docs_and_scores)

def manual_vector_check_with_filter():
    """
    指定したPDFだけを対象にした検索テスト
    """
    vectorstore = load_vectorstore()
    target_pdf = "about_sun.pdf"

    answer, docs_and_scores = get_answer(QUESTION, vectorstore, target_pdf=target_pdf)

    print("💬 質問:", QUESTION)
    print("📁 検索対象:", target_pdf)
    print("💡 回答:\n", answer)
    print_chunk_info_markdown(docs_and_scores)

def validate_source_format(docs_and_scores):
    """
    source に (p.N) が含まれているかどうかを機械的にチェック
    """
    print("\n✅ sourceフォーマット検証結果:")

    # ファイル名 + ページ番号が記録されていることを検証する
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
    # ✅ テストしたい方をコメントアウトで切り替える
    # manual_vector_check_all()
    manual_vector_check_with_filter()
    # validate_source_format(...) ← docs_and_scores が必要な場合に手動で呼び出し可
