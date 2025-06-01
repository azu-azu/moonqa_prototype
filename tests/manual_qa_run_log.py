# tests/manual_qa_run_log.py

from app.qa import load_vectorstore, get_answer
from tests.log_utils import append_json_log

if __name__ == "__main__":
    vectorstore = load_vectorstore()
    # question = "月って何？"
    # question = "月の特徴は？"
    # question = "月って、どうやってできたの？"
    # question = "地球とはどんな関係にあるの？"
    question = "なんか面白いこと教えて。"
    answer, docs_and_scores = get_answer(question, vectorstore)

    print("💬 質問:", question)
    print("💡 回答:", answer)
    print("\n🔍 スコア付き文書:\n")
    for doc, score in docs_and_scores:
        print(f"- score: {score:.3f}")
        print(f"  content: {doc.page_content[:100]}...\n")

    append_json_log(question, answer, docs_and_scores)
