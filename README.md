# ollama-oneshot-q

A context-free, disposable CLI assistant to ask quick questions without cluttering your main chat histories.  

セッションの会話履歴を汚さず、横道に逸れた簡単な質問をターミナルから実行

![demo](assets/readme.gif)

## 🛠️ セットアップ

### 1. クローンとインストール
リポジトリをローカルにクローンし、`pipx` を使ってインストールします。

```bash
git clone https://github.com/otohusan/ollama-oneshot-q.git
cd ollama-oneshot-q
pipx install -e .
```

※ `pipx` が存在しない場合は、[こちら](https://github.com/pypa/pipx#install-pipx)を参照してください

### 2. 初期セットアップの実行
対話形式で Ollama Cloud の API トークンを登録し、自動的に `.env` と `skill.md` を生成します。

```bash
oneshot-setup
```

実行後、どこからでも `q [質問内容]` で起動できるようになります。

## 💡 使い方

ターミナルから `q` コマンドに続けて質問を投げるだけです。

```bash
$ q 便利なシェルコマンド教えて
--- Q: 便利なシェルコマンド教えて ---
```

## 📝 プロンプトのカスタマイズ

`oneshot-setup` の実行によって、リポジトリのルートに `skill.md` が生成されます。
このファイルの記述を変更することで、AIの回答スタイルを自分好みに完全カスタマイズ可能です。

初期状態は `skill.md.example` に記載されています。

## 🔒 ライセンス

MIT License
