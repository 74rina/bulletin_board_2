# Frontend Development

## 1. Project Overview

この frontend は React + TypeScript + Vite で作られた匿名掲示板アプリです。主な画面は `App.tsx` にあり、投稿作成、投稿一覧、投稿詳細表示、コメント作成を扱います。

backend API とは HTTP 経由で通信します。API のベース URL は `VITE_API_BASE_URL` を優先し、未設定の場合は `http://localhost:8002` を使います。

作業時は frontend ディレクトリで以下を使います。

```bash
npm run dev
npm run build
npm run lint
```

## 2. Directory Structure

```text
frontend/
  src/
    App.tsx              # 掲示板画面、状態管理、API通信の中心
    App.css              # App.tsx 用の画面スタイル
    index.css            # グローバルCSS、CSS変数、基本要素のスタイル
    main.tsx             # Reactのエントリーポイント
    AGENTS.md            # frontend 開発ガイド
    assets/              # 画像やSVGなどの静的アセット
    components/          # 再利用コンポーネント置き場
```

新しいUI部品を追加するときは、まず `src/components/` に切り出せるかを考えます。画面全体の構成やデータ取得の責務は、必要以上に深い階層へ分散させないでください。

## 3. Coding Conventions

- TypeScript の strict 設定を前提にし、`any` は避けます。
- 既存コードに合わせて、import や文字列は single quote を使います。
- 既存コードに合わせて、文末の semicolon は付けません。
- React コンポーネントは function component で書きます。
- 型は、APIレスポンスやフォーム入力の意味が分かる名前にします。
- 未使用の変数、props、import を残しません。
- 日付表示などの小さな変換処理は、再利用されるなら関数として切り出します。
- 大きな変更をするときは、`npm run lint` と `npm run build` が通る状態にします。

## 4. Component Design

現在は `App.tsx` に多くの処理がまとまっています。機能追加で見通しが悪くなる場合は、以下の単位でコンポーネント化します。

- 投稿作成フォーム
- 投稿一覧
- 投稿カード
- 投稿詳細
- コメント一覧
- コメント作成フォーム
- エラーメッセージや空状態表示

コンポーネントを分けるときは、UI表示に必要な props を明確にします。子コンポーネントが API を直接呼ぶより、親で取得したデータとイベントハンドラを渡す形を優先します。

フォーム部品は controlled component として扱い、入力値は `useState` で管理します。

## 5. State Management

状態管理は React 標準の `useState`, `useEffect`, `useMemo` を基本にします。現時点では Redux や Zustand などのグローバル状態管理ライブラリは使いません。

状態は用途ごとに分けます。

- APIから取得したデータ: `posts`, `selectedPost`
- 選択中のID: `selectedPostId`
- ローディング状態: `loadingPosts`, `loadingPostDetail`
- エラー表示: `error`
- フォーム入力: `name`, `title`, `body`, `commentBody`

派生値は、必要に応じて `useMemo` を使います。ただし、単純な値まで過剰に `useMemo` 化しないでください。

## 6. API Integration

API通信は `fetch` を使います。エンドポイントは `API_BASE` を使って組み立て、URLを各所に直接書き散らさないでください。

現在使っている API は以下です。

- `GET /posts`
- `POST /posts`
- `GET /posts/{post_id}`
- `POST /posts/{post_id}/comments`

APIレスポンスの型は TypeScript の `type` で定義します。backend の response model が変わる場合は、frontend 側の型も同時に更新します。

POST では `Content-Type: application/json` を指定し、送信内容は `JSON.stringify` します。通信後に一覧や詳細を更新する必要がある場合は、既存の `fetchPosts` や `fetchPostDetail` を再利用します。

## 7. Error Handling

`fetch` の結果は `res.ok` を確認し、失敗時はユーザーに表示できるエラーメッセージを `error` state に入れます。

エラー文言は画面利用者向けの日本語にします。開発者向けの詳細な例外情報をそのまま画面に出さないでください。

通信開始前に関連するエラーをクリアし、`finally` でローディング状態を戻します。複数の通信が連続する処理では、どの表示を更新する必要があるかを確認してから state を変更します。

## 8. UI/UX Guidelines

既存UIは濃い緑系の背景、カード状のパネル、丸みのあるフォーム部品で構成されています。新しい要素を追加するときは、`index.css` の CSS variables と `App.css` の既存クラス設計に合わせます。

- 色は `--bg`, `--bg-card`, `--text`, `--text-muted`, `--accent`, `--border` などの変数を優先します。
- 余白、角丸、影は既存の `--radius-*` や `--shadow` に合わせます。
- ボタン、input、textarea の基本スタイルを壊さないようにします。
- 投稿やコメントがない場合は、空状態のメッセージを表示します。
- 読み込み中は、何が読み込み中か分かる表示にします。
- モバイル表示では、既存の media query と同じ breakpoint を意識します。
- クリック可能な要素は `button` を使い、キーボード操作やアクセシビリティを損なわないようにします。

## 9. Testing

現時点で frontend 専用のテストフレームワークは導入されていません。変更後は最低限以下を確認します。

```bash
npm run lint
npm run build
```

画面上では以下を手動確認します。

- 投稿一覧が取得できる
- 投稿を作成できる
- 投稿を選択すると詳細が表示される
- コメントを作成できる
- API停止時や失敗時にエラーメッセージが表示される
- 幅の狭い画面でもレイアウトが崩れない

テストを追加する場合は、フォーム入力、API失敗、空状態、ローディング状態のように、ユーザーに見える振る舞いを優先して検証します。
