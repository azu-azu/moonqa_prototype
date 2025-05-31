import json
import pytest
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

@pytest.mark.parametrize("query,target_pdf", [
    (q["question"], q.get("target_pdf")) for q in json.load(open("data/questions.json", encoding="utf-8"))
])
def test_similarity_search_with_threshold(query, target_pdf):
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

    # ✅ スコアしきい値（例：0.3未満は除外）
    threshold = 0.3
    filtered = [doc for doc, score in results if score >= threshold]

    # ✅ テスト判定
    assert len(filtered) > 0, f"No relevant documents for query: {query} (threshold={threshold})"
