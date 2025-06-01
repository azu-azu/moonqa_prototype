# 現在地
🗓️ 2025/05/31 \[Saturday] 12:10

✅ pytest対応テスト通過（1件）
✅ questions.jsonを正しい位置から読み込む形式に修正済み
✅ pytest導入完了（poetry --dev）
⚠ faiss + numpy関連のDeprecationあり（現時点では致命的でない）

---

# 🎯 テストケース追加
## 🔍 理由

| 項目                              | 理由                              |
| ------------------------------- | ------------------------------- |
| ✅ **回帰テストとしての価値**               | 異なる質問で壊れてないか検証できるようにしておくべき      |
| ✅ **target\_pdfが必要か否か**の判断材料になる | 質問を増やすことで、どのPDFがヒットするか明確になる     |
| ✅ **後続の`target_pdf`実装の前提**      | PDFごとに分離できるかをテストで把握してから設計するのが安全 |
| ✅ **CIでの価値が大きい**                | 多ケースでの自然言語テストは、CI自動化の一番の柱になる    |

---

## 📌 推奨ステップ

1. `data/questions.json` に3〜5件の多様な質問を追加（対象PDFが異なるものを意識）
2. `pytest` 実行で回答が返るかチェック
3. その上で、「PDFごとに制限したい」ニーズが出たら `target_pdf` 実装へ進む

---

## 現在地
✅ data/questions.json に7件の多様な質問を登録
✅ pytest形式での自動テスト成功（全件パス）
✅ 月と太陽に関連するQAの動作確認済み
⚠ numpy + faiss 警告は引き続き存在（構造には影響なし）

## Next
👉 `target_pdf` 対応 | 検索対象PDFを制限したいときに

---

# 📘 Phase 3：PDFを指定して検索対象を絞る機能（target\_pdf）を実装し、テストで検証可能にする
🗓️ 2025/05/31 \[Saturday] 12:37

---

## ✅ Step 1: `questions.json` に target\_pdf を追加

### ✏ 新形式（拡張）

```json
[
  {
    "question": "月って何？",
    "target_pdf": "about_moon.pdf"
  },
  {
    "question": "太陽はどうやって光ってるの？",
    "target_pdf": "about_sun.pdf"
  },
  {
    "question": "なんか面白いこと教えて。",
    "target_pdf": null
  }
]
```

※ `"target_pdf"` が `null` か未指定なら全体検索、指定されてたらそのPDFのみ検索。

---

## ✅ Step 2: test_qa_search.py の改修

### 🔧 修正ポイント案｜`target_pdf` 対応 RetrievalQA chain を作る

| 変更点                                 | 内容                           |
| ----------------------------------- | ---------------------------- |
| `build_qa_chain()` 関数化              | target_pdf指定を柔軟に制御          |
| `retriever.search_kwargs["filter"]` | メタデータ `"source"` に対してフィルタを適用 |
| `pytest.mark.parametrize()`         | 各質問に対して target\_pdf を動的に割り当て |


---

### ✅ 実行結果
**target\_pdf フィルタ付きで 7件全部パス**

| 項目                                             | 状況       |
| ---------------------------------------------- | -------- |
| `questions.json` を `target_pdf` 対応に変更          | ✅ 完了     |
| `test_qa_search.py` を chain + parametrize で構造化 | ✅ 完了     |
| `retriever.search_kwargs["filter"]` によるPDF指定検索 | ✅ 動作確認済み |
| pytest 実行結果（7件パス）                              | ✅ 成功！    |

---

## 📘 Phase 3：進行ログ更新

```
✅ Step 1: 質問ごとに対象PDFを指定する形式に移行
✅ Step 2: テストコードを target_pdf に対応
✅ Step 3: 全件テスト通過を確認（filterの実動作含む）
🟡 次ステップ：スコア閾値の導入 or ログ可視化
```

# スコアしきい値の導入｜類似度スコアが低すぎる結果（＝関係ない文書）を除外できるようにして、回答の質をコントロールする
## ✅ テスト結果まとめ

| 要素                                     | 内容                 |
| -------------------------------------- | ------------------ |
| `similarity_search_with_score()` に切り替え | ✅ 完了               |
| `score >= 0.3` のしきい値導入                 | ✅ 効いている            |
| 7件すべて通過（フィルタ後でも結果あり）                   | ✅ フィルタが厳しすぎず、十分ヒット |
| Deprecation warnings                   | ⚠ 引き続き出てるが問題なし     |

---

## 📘 Phase 3 最終ログ

```
✅ target_pdf のフィルタ機能 導入・検証済み
✅ score_threshold による精度制御 導入・動作確認済み
✅ 自動テストへの組み込み 完了
📦 検索の構造を RetrievalQA から ベクトル直検索に最適化済み
```

---

## 🏁 結論：**Phase 3 完了！！**

```text
Phase 3: 精度向上＆制御強化 → ✅ 完了
```

---

# 📘 Phase 4：ログと可視化


## `test_qa_search.py` に `--log-output` オプションでログ出力を切り替えられるようにする
> このテストは、「LangChain + FAISS」における“意味ベースの文書検索”が、意図どおり動いているかを保証する構造的品質テスト。
つまりこれが通らなかったら、「AIはそれっぽく答えてるだけ」。
精度を持った検索ベースQAとして、今後の展開（UI・CI・可視化）にもつなげられる基盤とする。

### 🔍 このテストで何がわかったか？
#### 1. **スコアしきい値のフィルタが正しく動作している**

* `score_threshold = 0.3` を明示的に設定して、
* **0.3以上の類似スコアを持つチャンクが最低1つはあるか**をチェック。
* → これは、**ゴミ回答を防ぐ品質の防波堤**。

#### 2. **retrieverのfilter（source指定）が正しく働いてる**

* `retriever.search_kwargs["filter"] = {"source": target_pdf}`
* → これで **質問と対象PDFの対応が合ってるか**を担保できた。

#### 3. **ログ出力が構造的に記録されている**

* 質問、スコア、該当チャンク、出典PDF、timestamp まで。
* → これは後工程（UI連携・エラー分析・精度分析）に重要。

---

### なぜこのテストが重要か？
* このテストは「**意味の近さ（cosine類似度）に基づく構造的判断**が、実装どおりに機能しているか？」を確かめるテスト。
* 「LangChain QAは意味を理解してるように“見える”けど、実は全然関係ない文を返してた」ってことを防ぐ設計。

### QAアプリの**精度の根拠**を担保
* 類似度しきい値のテストは、**精度保証の最低ライン**。
* 「意味が近いかどうか」を自動で見極めるロジックが、ちゃんと働いてることを証明した。

---


# 📘 Phase 4 - Task 3: ログ出力の品質チェックと可視化の土台
🗓️ 2025/05/31 \[Saturday] 20:50

## ✅ 現状の構造（抜粋）

```json
{
  "timestamp": "2025-05-31T11:25:34.273507",
  "query": "太陽って何？",
  "target_pdf": "about_sun.pdf",
  "results": [ ... ]
}
```

---

## 🎯 Task Name：`query_id` の導入と設計反映

### Cause Summary
ログを後から分析・UI連携する際に、`query_id` がないと一致・追跡が難しくなるため。

### Possible Causes
* 現在は `query` が文字列としてそのまま保存されているだけで、一意識別ができない。
* 質問文が重複する場合などに整合性が取れない。

### Action Plan
1. `questions.json` に `id` を追加する（形式：`q001`, `q002`, …）
2. `test_qa_search.py` 側のループで `query_id` をログに含める
3. ログ出力先（`qa_log.jsonl`）の構造に `query_id` を追記する
4. JSONLの出力確認（pytest 通常実行でOK）

### Structural Note
* **命名規則**は固定長（例：`q003`）にしておくと、UIでの並び順や整合確認がしやすい。
* 今回は `questions.json` 側を編集し、それを元に `test_qa_search.py` で使う。

### 修正対象: tests/test_qa_search.py
変更点まとめ：
question_obj から id を取り出して query_id としてログに追加
ログ出力する辞書に query_id キーを追加

### 🎯 このテストの確認ポイント
- `query_id` を含めた JSON ログが、正常に出力されるかを検証する
- ログ出力ファイル：`logs/qa_log.jsonl`

### テスト結果
* `test_qa_search.py` がエラーなく **7件すべての質問に対して実行成功**
* `--log-output` オプションを指定したため、**各質問のログが出力された**
* `query_id` 対応のコードで実行されている（確認済）

### まとめ：このテストで得られた信頼性
* ログ出力が機能する
* `query_id` が付与される
* ログ構造が壊れていない
* pytestオプション制御が有効


## 🎯 Task Name：filter導入

### 実行結果
* **スコア 0.2022 / 0.2871 → 両方しきい値 0.2 超え ✅**
* `source: about_sun.pdf (p.1)` → **ちゃんとフィルター効いてる！**
* `content:` に「光が太陽から地球に届くまで約 8 分 19 秒」→ **どんぴしゃ回答あり！**

---

### 成功までのエラー原因
* retriever に filter 渡してた → retriever.search_kwargs["filter"] = {"source": target_pdf}
* 正しくは、dbにfilterかける → results = db.similarity_search_with_score(query, k=3, filter=...)

* `metadata["source"]` に対して filter してたのが間違いだった
* → `metadata["pdf_name"]` に修正したら、狙い通りのPDFだけ検索できた

---

### 💡 ふりかえりメモ

* 表示用とフィルタ用で `metadata` を分ける設計にする
* `"表示 = source"` / `"フィルタ = pdf_name"` というルール
* テスト失敗時は、「どんなメタデータで保存されたか」を確認するのが第一

| 用途    | フィールド名     | 値の例                   |
| ----- | ---------- | --------------------- |
| フィルタ用 | `pdf_name` | `about_sun.pdf`       |
| 表示用   | `source`   | `about_sun.pdf (p.1)` |


---

## 🎯 Task Name：（Phase 4/Task 3） `timestamp`実装
🗓️ 2025/06/01 \[Sunday] 9:00

### 1. `timestamp` の付与方法を決める
→ 各 `query_id` ごとに `datetime.now()`

### 2. ログ出力のdict構造を作成する
```python
log_entry = {
    "query_id": query_id,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "score": score,
    "source": f"{pdf_name} (p.{page_number})",
    "content": chunk_content
}
```

### 3. `save_log_entry()` を作成して `logs/qa_log.jsonl` に追記する
（存在しないときはディレクトリ作成含む）

### 4. `--log-output` または `log_output_enabled` に連動して保存有無を制御する


### 方針

* `tests/test_qa_search.py` に統合する
* `argparse` で `--log-output` オプションを使ってるなら、`args.log_output` を受け取る
* その上で `save_log_entry()` を条件分岐で呼ぶだけでOK

---

### テスト結果

**Task 3：ログ出力の品質チェックと可視化の土台 → 完全完了**

* ✅ JSONL形式に準拠
* ✅ timestamp対応済（フォーマットも◎）
* ✅ 本番コードとの責務分離も完了（`qa.py`に混在なし）
* ✅ `manual_qa_run_log.py` での動作確認OK
