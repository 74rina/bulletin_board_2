# 匿名掲示板アプリ

FastAPI + PostgreSQL + React (Vite) で構成した匿名掲示板アプリです。投稿とコメントのCRUDを提供します。

## 構成

- backend: FastAPI + SQLAlchemy + Alembic
- frontend: React + Vite
- db: PostgreSQL

## 主要機能

- 投稿作成
- 投稿一覧
- 投稿詳細
- コメント作成

## API

- `POST /posts`
- `GET /posts`
- `GET /posts/{post_id}`
- `POST /posts/{post_id}/comments`

## チーム開発での環境構築

### 前提

- Docker Desktop をインストール済み
- ポートの競合がないこと
  - frontend: `5174`
  - backend: `8002`
  - db: `5433`

### 1. リポジトリ取得

```
git clone <REPO_URL>
cd bulletin_board_2
```

### 2. 環境変数の用意

```
cp .env.example .env
```

`.env` の内容はチーム内で共通にしておくと動作が揃います。

### 3. 起動

```
docker compose up -d --build
```

### 4. アクセス

- frontend: `http://localhost:5174`
- backend: `http://localhost:8002`

## マイグレーション

### 生成

```
docker compose exec -T backend alembic revision --autogenerate -m "<message>"
```

### 適用

```
docker compose exec -T backend alembic upgrade head
```

### 巻き戻し

```
docker compose exec -T backend alembic downgrade -1
```

## 開発メモ

- DB 接続は `DATABASE_URL` または `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME` を参照します。
- CORS は `http://localhost:5173` と `http://localhost:5174` を許可しています。

## トラブルシューティング

### 5173 が別アプリで使われている

ホストの 5173 を使っているプロセスを停止するか、`docker-compose.yml` で別ポートを割り当ててください。

```
lsof -nP -iTCP:5173 -sTCP:LISTEN
kill -9 <PID>
```

### フロントで 500 が出る

- 別アプリが 5173 を掴んでいる可能性があります。
- `http://localhost:5174` でアクセスしてください。

## ディレクトリ構成

```
.
├── backend
│   ├── app
│   ├── alembic
│   └── requirements.txt
├── frontend
│   ├── src
│   └── package.json
└── docker-compose.yml
```
