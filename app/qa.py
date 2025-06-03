# app/qa.py

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate
from app.config import get_index_path
from app.settings import SCORE_THRESHOLD, OPENAI_MODEL
from app.logger import build_log_entry, append_qa_log

MISSING_ANSWER = "データの中に、今回の答えはなかったみたいやわ。ごめんやで🌙"

# プロンプトテンプレート（関西弁・句点改行スタイル）
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
    """
    FAISSベクトルストアをローカルから読み込む。
    """
    embedding = OpenAIEmbeddings()
    return FAISS.load_local(get_index_path(), embedding, allow_dangerous_deserialization=True)

def retrieve_relevant_docs(vectorstore, query, target_pdf=None):
    """
    質問に対して類似チャンクを取得する。

    - target_pdf が指定されていれば、そのPDFだけを対象にする（source に部分一致）
    - SCORE_THRESHOLD 以下のチャンクのみ返す（距離が近いもの）
    """
    search_kwargs = {"k": 5}
    docs_and_scores = vectorstore.similarity_search_with_score(query, **search_kwargs)

    if target_pdf:
        docs_and_scores = [
            (doc, score) for doc, score in docs_and_scores
            if target_pdf in doc.metadata.get("source", "")
        ]

    filtered = [(doc, score) for doc, score in docs_and_scores if score <= SCORE_THRESHOLD]
    return filtered

def format_docs(docs):
    """
    チャンクを文字列として結合
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(question, vectorstore, target_pdf=None):
    """
    指定された質問に対して回答を返す。
    質問 → ドキュメント検索 → プロンプト → 回答生成

    - target_pdf を指定すると、そのPDFのみを検索対象にする。
    - sourceやチャンク内容の確認は含まれない。
    - それらを確認したい場合は manual_vector_check.py を使用。
    """
    docs_and_scores = retrieve_relevant_docs(vectorstore, question, target_pdf)

    if not docs_and_scores:
        # 回答が見つからなかった場合
        log_entry = build_log_entry(
            question=question,
            answer="",
            results=[],
            status="notfound",
            intent=None
        )
        append_qa_log(log_entry)
        return MISSING_ANSWER, []

    docs = [doc for doc, _ in docs_and_scores]
    context = format_docs(docs)

    chain = RunnableMap({
        "context": lambda _: context,
        "question": lambda _: question
    }) | PROMPT_TEMPLATE | ChatOpenAI(model=OPENAI_MODEL, temperature=0)

    result = chain.invoke({})
    sources = ", ".join(sorted(set(doc.metadata.get("source", "?") for doc in docs)))
    full_answer = result.content + "\n\n参照元：" + sources

    # 回答が見つかった場合（成功）
    log_entry = build_log_entry(
        question=question,
        answer=full_answer,
        results=[{
            "source": doc.metadata.get("source"),
            "score": float(score)  # float32 → float に変換
        } for doc, score in docs_and_scores],
        status="success",
        intent=None
    )
    append_qa_log(log_entry)

    return full_answer, docs_and_scores
