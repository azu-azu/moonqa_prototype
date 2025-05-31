import json
import pytest
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# ✅ ログ出力フラグを pytest オプションから取得
# --log-output を付けたときだけ logs/qa_log.jsonl に追記される
def pytest_addoption(parser):
    parser.addoption("--log-output", action="store_true", help="Enable log output")

# ✅ テスト関数内で使用できるように fixture を定義
@pytest.fixture
def log_output_enabled(request):
    return request.config.getoption("--log-output")

# ✅ ログ出力関数
def append_log_entry(query, target_pdf, results):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "target_pdf": target_pdf,
        "results": [
            {
                "score": float(score),  # float32 → float 変換でJSON対応
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc, score in results
        ]
    }

    with open("logs/qa_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# ✅ パラメータ化テスト（JSONの全質問）
@pytest.mark.parametrize("query,target_pdf", [
    (q["question"], q.get("target_pdf")) for q in json.load(open("data/questions.json", encoding="utf-8"))
])
def test_similarity_search_with_threshold(query, target_pdf, log_output_enabled):
    db = FAISS.load_local(
        folder_path="index/faiss_index",
        embeddings=OpenAIEmbeddings(),
        index_name="index",
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever()
    if target_pdf:
        retriever.search_kwargs["filter"] = {"source": target_pdf}

    # ✅ スコア付き検索（RetrievalQAは使わない）
    results = db.similarity_search_with_score(query, k=3)

    # ✅ スコアしきい値
    threshold = 0.3
    filtered = [doc for doc, score in results if score >= threshold]

    # ✅ テスト：しきい値以上が1件以上ヒットすること
    assert len(filtered) > 0, f"No relevant documents for query: {query} (threshold={threshold})"

    # ✅ ログ出力はオプション付きのときだけ
    if log_output_enabled:
        append_log_entry(query, target_pdf, results)
