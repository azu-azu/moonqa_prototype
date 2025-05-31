# app/qa.py

import os
import json
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate
from app.config import get_index_path
from app.settings import SCORE_THRESHOLD, OPENAI_MODEL

# プロンプトテンプレート
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    (
        "system",
        "あなたは、関西弁のやわらかい語り口で話すアシスタントです。\n"
        "口調はフレンドリーで、優しく寄り添うように話してください。\n"
        "文体は『です・ます調』は使わず、句点（。）で改行してください。\n"
        "読点（、）では改行しないでください。\n"
        "詩的すぎる表現は避け、ふんわりした関西弁で、リズムよく3〜7行でまとめてください。\n"
    ),
    (
        "human",
        "{context}\n\n質問: {question}"
    )
])

def load_vectorstore():
    embedding = OpenAIEmbeddings()
    return FAISS.load_local(get_index_path(), embedding, allow_dangerous_deserialization=True)

def retrieve_relevant_docs(vectorstore, query):
    docs_and_scores = vectorstore.similarity_search_with_score(query, k=5)
    # スコアが小さい（距離が近い）ものを残す
    filtered = [(doc, score) for doc, score in docs_and_scores if score <= SCORE_THRESHOLD]
    return filtered

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(question, vectorstore):
    """
    指定された質問に対して回答を返す軽量関数。
    - sourceやチャンク内容の確認は含まれません。
    - それらを確認したい場合は manual_vector_check.py を使用してください。
    """

    docs_and_scores = retrieve_relevant_docs(vectorstore, question)
    if not docs_and_scores:
        return "データの中に、今回の答えはなかったみたいやわ。ごめんやで🌙", []

    docs = [doc for doc, _ in docs_and_scores]
    context = format_docs(docs)

    chain = RunnableMap({
        "context": lambda _: context,
        "question": lambda _: question
    }) | PROMPT_TEMPLATE | ChatOpenAI(model=OPENAI_MODEL, temperature=0)

    result = chain.invoke({})
    sources = ", ".join(sorted(set(doc.metadata.get("source", "?") for doc in docs)))
    full_answer = result.content + "\n\n参照元：" + sources

    return full_answer, docs_and_scores

def append_json_log(question, answer, docs_and_scores):
    log_entry = {
        "question": question,
        "answer": answer,
        "documents": [
            {
                "content": doc.page_content,
                "score": float(score),
                "source": doc.metadata.get("source", "unknown")
            }
            for doc, score in docs_and_scores
        ]
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/qa_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# 使用チャンク情報を Markdown形式で出力
def print_chunk_info_markdown(docs_and_scores):
    print("\n## 🔍 使用チャンク情報\n")
    for i, (doc, score) in enumerate(docs_and_scores):
        source = doc.metadata.get("source", "unknown")
        print(f"### Chunk {i+1}")
        print(f"- **Score**: {score:.4f}")
        print(f"- **Source**: {source}")
        print(f"```\n{doc.page_content.strip()[:500]}\n```") # 長すぎる本文は500文字まで
        print()
