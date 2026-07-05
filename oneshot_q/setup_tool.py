import sys
from pathlib import Path

# python-dotenv のインポート（インストールチェック付き）
try:
    from dotenv import set_key
except ImportError:
    print("❌ エラー: `python-dotenv` が見つかりません。")
    print("先に `pipenv install` を実行して依存関係をインストールしてください。")
    sys.exit(1)

# パスの定義
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
SKILL_PATH = BASE_DIR / "skill.md"
TEMPLATE_PATH = BASE_DIR / "skill.md.template"


def ask_yes_no(question: str) -> bool:
    """Yes/No の入力を受け付けるヘルパー関数"""
    while True:
        reply = input(f"{question} (y/n): ").strip().lower()
        if reply in ["y", "yes"]:
            return True
        if reply in ["n", "no"]:
            return False
        print("❌ 'y' または 'n' で入力してください。")


def main():
    print("========================================")
    print(" 🛠️  Ollama Q-CLI 初期セットアップ")
    print("========================================")

    # 1. APIトークンの入力と .env の作成
    print("\n[Step 1: API トークンの設定]")
    token = input("🔑 Ollama Cloud の APIトークンを入力してください:\n> ").strip()

    if not token:
        print(
            "❌ エラー: トークンが入力されなかったため、セットアップを中断しました。",
            file=sys.stderr,
        )
        sys.exit(1)

    # .env ファイルの作成と書き込み
    if not ENV_PATH.exists():
        ENV_PATH.touch()

    try:
        set_key(str(ENV_PATH), "OLLAMA_CLOUD_TOKEN", token)
        print("✨ .env ファイルにトークンを正常に保存しました。")
    except Exception as e:
        print(
            f"❌ .env への書き込み中にエラーが発生しました: {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    print("-" * 40)

    # 2. skill.md の作成確認
    print("[Step 2: プロンプト設定ファイルの作成]")
    if not TEMPLATE_PATH.exists():
        print(
            "⚠️ 警告: skill.md.example が見つからないため、このステップをスキップします。"
        )
        return

    if SKILL_PATH.exists():
        print("💡 すでに skill.md が存在するため、作成をスキップします。")
        return

    create_skill = ask_yes_no(
        "📝 テンプレートから skill.md（短文回答用のルール設定）を作成しますか？"
    )
    if not create_skill:
        print("⏭️  skill.md の作成をスキップしました。")
        return

    try:
        skill_content = TEMPLATE_PATH.read_text(encoding="utf-8")
        SKILL_PATH.write_text(skill_content, encoding="utf-8")
        print("✨ skill.md を作成しました！（後から自由に変更できます）")
    except Exception as e:
        print(f"⚠️ skill.md の作成中にエラーが発生しました: {e}", file=sys.stderr)

    # 3. セットアップ完了とエイリアスの案内
    print("========================================")
    print("🎉 セットアップが正常に完了しました！")
    print("========================================")
    print("\n最後に、ターミナルから `q` で一発起動できるように設定を行います。")
    print(
        "👉 お使いのシェル（~/.zshrc や ~/.bashrc など）の末尾に、以下の1行をコピペして保存してください:\n"
    )

    print("-" * 70)
    # 現在の絶対パスを自動で埋め込んだエイリアスを表示
    print(f'alias q="pipenv run --rmat {BASE_DIR} python3 {BASE_DIR / "q.py"}"')
    print("-" * 70)

    print(
        "\n設定を反映させるには、`source ~/.zshrc` を実行するか、ターミナルを再起動してください。"
    )
    print("いつでも `q [質問内容]` で爆速アシスタントが起動します！\n")


if __name__ == "__main__":
    main()
