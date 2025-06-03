# app/classifier.py

from typing import Literal

# Literal[...] を使うことで返り値の型も明確化
# この関数の返り値は、Literal[...] の中のどれかしか許されない
IntentType = Literal["pdf_question", "chitchat", "command"]

def classify_intent(question: str) -> IntentType:
    """
    質問の内容に応じて intent を分類する。
    ルールベースで判定（単語・構文に応じてざっくり分類）
    """
    q = question.lower()

    # ① command（命令系）
    command_keywords = [
        "削除", "消して", "取り消して", "再構築", "もう一回", "保存", "出力して",
        "ingest", "reload", "index作成", "再実行"
    ]
    if any(word in q for word in command_keywords):
        return "command"

    # ② chitchat（世間話・感情・雑談）
    chitchat_keywords = [
        "疲れた", "しんどい", "眠い", "つらい", "孤独", "やる気ない", "暇", "話そう", "最近どう",
        "ムカつく", "嬉しい", "楽しい", "悲しい", "寂しい", "彼氏", "恋愛", "夢", "将来"
    ]
    if any(word in q for word in chitchat_keywords):
        return "chitchat"

    # ③ pdf_question（それ以外は基本PDFとみなす）
    return "pdf_question"
