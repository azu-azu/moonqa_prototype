import os
import json
import pytest
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from tests.log_utils import validate_log_entry

# ✅ ログ出力フラグを pytest オプションから取得
# --log-output を付けたときだけ logs/qa_log.jsonl に追記される
def pytest_addoption(parser):
    parser.addoption("--log-output", action="store_true", help="Enable log output")

# ✅ テスト関数内で使用できるように fixture を定義
@pytest.fixture
def log_output_enabled(request):
    return request.config.getoption("--log-output")

# ✅ ログ出力関数（query_id 含む）
def append_log_entry(query_id, query, target_pdf, results):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query_id": query_id,
        "question": query,
        "target_pdf": target_pdf,
        "result_count": len(results),
        "results": [
            {
                "score": float(score), # float32 → float 変換でJSON対応
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc, score in results
        ]
    }

    with open("logs/qa_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# ✅ 質問データ読み込み＆パラメータ化
@pytest.mark.parametrize("query_id,query,target_pdf", [
    (q["id"], q["question"], q.get("target_pdf")) for q in json.load(open("data/questions.json", encoding="utf-8"))
])
def test_similarity_search_with_threshold(query_id, query, target_pdf, log_output_enabled):
    # db = “ベクトルストア” インスタンス
    # ここで得られる db は、直接 .similarity_search_with_score() や .similarity_search() を実行できる検索オブジェクト
    db = FAISS.load_local(
        folder_path="index/faiss_index",
        embeddings=OpenAIEmbeddings(),
        index_name="index",
        allow_dangerous_deserialization=True
    )

    # ✅ filterを正しく渡す（retrieverは使わない）
    search_kwargs = {"k": 3}
    if target_pdf:
        search_kwargs["filter"] = {"pdf_name": target_pdf}

    results = db.similarity_search_with_score(query, **search_kwargs)

    # ✅ スコアしきい値確認ログ
    threshold = 0.2
    for doc, score in results:
        print(f"[{query_id}] Score: {score:.4f} → {'✔︎' if score >= threshold else '×'}")
        print(f"source: {doc.metadata.get('source')}")
        print(f"content: {doc.page_content[:80]}")  # 長すぎるときは80文字で切って確認
        print("-" * 50)

    # ✅ スコアしきい値フィルタ
    filtered = [doc for doc, score in results if score >= threshold]

    assert len(filtered) > 0, f"No relevant documents for query_id: {query_id} (threshold={threshold})"

    # ✅ ログ出力
    if log_output_enabled:
        append_log_entry(query_id, query, target_pdf, results)


def test_log_entry_structure():
    log_path = "logs/qa_log.jsonl"
    if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
        pytest.skip("🌒ログが存在しないためスキップしたんよ")
    validate_log_entry(log_path)