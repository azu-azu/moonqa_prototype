# conftest.py
# pytest が自動で読み込む特殊ファイル
# どのテストファイルにも共通して効かせたい処理を書く

def pytest_addoption(parser):
    parser.addoption(
        "--log-output",
        action="store_true",
        default=False,
        help="Enable log output to file"
    )
