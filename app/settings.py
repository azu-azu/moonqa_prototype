# app/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAIモデルの指定（環境変数から取得）
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# 類似スコアの閾値（0.0〜1.0の範囲で調整可能）
SCORE_THRESHOLD = 0.6