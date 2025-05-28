# app/qa.py

import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate
from app.config import get_index_path
from app.settings import SCORE_THRESHOLD, OPENAI_MODEL

# プロンプトテンプレート
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", "以下の情報に基づいて、質問に日本語で簡潔に答えてください。\n情報が不十分な場合は「検索スコアが低いため、十分な根拠が見つかりませんでした」と答えてください。"),
    ("human", "{context}\n\n質問: {question}")
])

def load_vectorstore():
    embedding = OpenAIEmbeddings()
    return FAISS.load_local(get_index_path(), embedding, allow_dangerous_deserialization=True)

def retrieve_relevant_docs(vectorstore, query):
    docs_and_scores = vectorstore.similarity_search_with_score(query, k=3)
    filtered = [(doc, score) for doc, score in docs_and_scores if score >= SCORE_THRESHOLD]
    return filtered

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(question, vectorstore):
    docs_and_scores = retrieve_relevant_docs(vectorstore, question)
    if not docs_and_scores:
        return "検索スコアが低いため、十分な根拠が見つかりませんでした。", []

    docs = [doc for doc, _ in docs_and_scores]
    context = format_docs(docs)

    chain = RunnableMap({
        "context": lambda _: context,
        "question": lambda _: question
    }) | PROMPT_TEMPLATE | ChatOpenAI(model=OPENAI_MODEL, temperature=0)

    result = chain.invoke({})
    return result.content, docs_and_scores

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
