from datetime import datetime
from typing import List

from pydantic import BaseModel


# TODO(p1): 投稿作成スキーマに名前・タイトル・本文の最小文字数と最大文字数のルールを追加する。frontend 影響あり。
# TODO(p3): 投稿作成スキーマにSwagger UIで試せるサンプル値を追加する。
class PostCreate(BaseModel):
    name: str
    title: str
    body: str


# TODO(p1): コメント作成スキーマに本文の最小文字数と最大文字数のルールを追加する。frontend 影響あり。
class CommentCreate(BaseModel):
    body: str


class CommentOut(BaseModel):
    # TODO(p2): コメントのレスポンスに post_id を含めるか検討し、必要ならAPIの形を揃える。frontend 影響あり。
    id: int
    body: str
    created_at: datetime

    class Config:
        from_attributes = True


class PostListItem(BaseModel):
    # TODO(p3): 投稿一覧で本文を全文返すか抜粋だけ返すかを決める。frontend 影響あり。
    id: int
    name: str
    title: str
    body: str
    created_at: datetime
    # TODO(p3): comment_count が0以上であることをレスポンススキーマで表現する。
    comment_count: int

    class Config:
        from_attributes = True


class PostDetail(BaseModel):
    # TODO(p3): 投稿詳細レスポンスにコメント件数を含め、一覧と詳細で表示情報を揃える。frontend 影響あり。
    id: int
    name: str
    title: str
    body: str
    created_at: datetime
    # TODO(p3): コメントが多い投稿でも扱いやすいレスポンス形式を考える。frontend 影響あり。
    comments: List[CommentOut]

    class Config:
        from_attributes = True


# TODO(p2): 投稿更新用のリクエストスキーマを追加し、必須項目と任意項目の違いを学べるようにする。frontend 影響あり。
# TODO(p2): コメント更新用のリクエストスキーマを追加し、作成時と更新時の入力ルールの違いを学べるようにする。frontend 影響あり。
# TODO(p2): 共通エラーレスポンスのスキーマを追加し、APIの失敗時の形を揃える。frontend 影響あり。
