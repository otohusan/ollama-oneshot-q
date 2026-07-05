#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from ollama import Client

# python-dotenv のインポート（インストールチェック付き）
try:
    from dotenv import load_dotenv
except ImportError:
    print(
        "❌ エラー: `python-dotenv` が見つかりません。先に `pipenv install` を実行してください。",
        file=sys.stderr,
    )
    sys.exit(1)

# パスの定義
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
SKILL_PATH = BASE_DIR / "skill.md"


DEFAULT_MODEL = "gpt-oss:120b"


def load_skills() -> str:
    """同ディレクトリ内にある skill.md の中身を自動でコンテキストとして読み込む"""
    if not SKILL_PATH.exists():
        return ""

    try:
        return SKILL_PATH.read_text(encoding="utf-8") + "\n"
    except Exception as e:
        print(f"⚠️ skill.md の読み込み中にエラーが発生しました: {e}", file=sys.stderr)
        return ""


def main():
    # 1. 環境変数の読み込み
    if not ENV_PATH.exists():
        print(
            "❌ エラー: .env ファイルが見つかりません。先に `pipenv run python3 setup.py` を実行してください。",
            file=sys.stderr,
        )
        sys.exit(1)

    load_dotenv(dotenv_path=ENV_PATH)
    ollama_token = os.environ.get("OLLAMA_CLOUD_TOKEN")
    model = os.environ.get("MODEL", DEFAULT_MODEL)

    if not ollama_token:
        print(
            "❌ エラー: .env 内に OLLAMA_CLOUD_TOKEN が設定されていません。setup.py を再実行してください。",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2. ユーザー入力とシステムコンテキストの準備
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "何か雑に考えて"
    system_context = load_skills()

    # 3. メッセージ構造の組み立て
    messages = []
    if system_context:
        messages.append(
            {
                "role": "system",
                "content": f"以下の知識やルールを前提として回答してください:\n{system_context}",
            }
        )
    messages.append({"role": "user", "content": user_input})

    print(f"--- Q: {user_input} ---\n")

    # 4. Ollama クライアントの初期化と実行
    try:
        client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {ollama_token}"},
        )

        # ストリーミング実行
        for part in client.chat(model=model, messages=messages, stream=True):
            print(part["message"]["content"], end="", flush=True)
        print("\n")

    except KeyboardInterrupt:
        print("\n\n🛑 [ストリーミングを中断しました]")
    except Exception as e:
        print(f"\n❌ エラー: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
