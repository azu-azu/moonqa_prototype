# app/filters.py

from typing import List, Tuple, Dict
from langchain_core.documents import Document

def filter_docs_by_metadata(
    docs_and_scores: List[Tuple[Document, float]],
    filter_dict: Dict[str, str]
) -> List[Tuple[Document, float]]:
    """
    メタデータに基づいてチャンクをフィルターする。

    - filter_dict に含まれる key/value 条件をすべて満たすチャンクのみを返す。
    - 各 key は、Document.metadata に含まれることが前提。
    - value は「部分一致」で判定する。

    例:
    filter_dict = {
        "source": "about_moon",
        "tag": "science",
        "date": "2025"
    }
    """
    def matches(doc: Document) -> bool:
        for key, expected in filter_dict.items():
            actual = doc.metadata.get(key, "")
            if expected not in str(actual):  # 部分一致
                return False
        return True

    return [
        (doc, score)
        for doc, score in docs_and_scores
        if matches(doc)
    ]
