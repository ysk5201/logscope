# logscope

Cisco形式のsyslog (`%ASA-4-106023: ...` のような行) を、severity とメッセージID別に集計するCLIツールです。
GitHub Actions と SRE の基礎を練習するための題材として作っています。

```
$ logscope samples/asa.log --max-severity 4
total: 14 lines (parsed 13, unparsed 1)

by severity:
  1 alerts              1
  2 critical            1
  3 errors              2
  4 warnings            3

top 10 message ids:
  ASA-4-106023              3
  ...
```

## ローカルで動かす

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pytest                       # テスト
ruff check . && ruff format --check .   # lint
logscope samples/asa.log --json
```

## GitHubに上げてActionsを動かす

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:<あなたのユーザー名>/logscope.git
git push -u origin main
```

push するとリポジトリの **Actions** タブで CI が走ります。
わざとテストを壊したブランチで PR を作り、CI が赤くなるのを確認してみてください。

## 練習課題 (順番にやるのがおすすめ)

### Step 1: Actions の基本
- [ ] README に CI のステータスバッジを貼る
- [ ] main ブランチに保護ルールを設定し、CI が通らないとマージできないようにする
- [ ] `pytest --cov-report=xml` を出して、`actions/upload-artifact` でカバレッジを保存する
- [ ] 機能追加: 時刻 (`Oct 17 10:15:05`) もパースして、分単位の件数を出す `--timeline` オプション

### Step 2: リリースとコンテナ
- [ ] `v*` タグの push で GitHub Release を自動作成する workflow (`release.yml`)
- [ ] Dockerfile を書き、Actions でビルドして ghcr.io に push する
- [ ] Trivy でイメージをスキャンし、Critical があれば失敗させる

### Step 3: セキュリティ強化 (DevSecOps)
- [ ] Dependabot (`.github/dependabot.yml`) で pip と GitHub Actions を自動更新
- [ ] CodeQL を有効化
- [ ] サードパーティ Action を `@v4` ではなくコミット SHA で固定する

### Step 4: SRE っぽくする
- [ ] FastAPI で `/summary` API 化し、Prometheus 形式の `/metrics` を出す
- [ ] OIDC 連携で Cloud Run (または AWS) に自動デプロイ
- [ ] `schedule` トリガーで API の外形監視をし、失敗したら Issue を自動作成

## Severity 一覧

| 値 | 名前 |
|---|---|
| 0 | emergencies |
| 1 | alerts |
| 2 | critical |
| 3 | errors |
| 4 | warnings |
| 5 | notifications |
| 6 | informational |
| 7 | debugging |
