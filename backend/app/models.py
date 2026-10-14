from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# TODO(p2): 投稿テーブルに更新日時を追加し、作成日時と更新日時の違いを扱えるようにする。frontend 影響あり。
class Post(Base):
    __tablename__ = "posts"

    # TODO(p3): 主キーに対する index=True の必要性を調べてモデル定義を整理する。
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # TODO(p1): 名前の最大長をスキーマとDBで同じルールに揃える。frontend 影響あり。
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    # TODO(p1): タイトルの最大長をスキーマとDBで同じルールに揃える。frontend 影響あり。
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # TODO(p2): 本文の空文字禁止や長さの上限をDB側でも表現する。
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # TODO(p2): 作成日時のタイムゾーンがAPIレスポンスで期待どおり扱われることを確認するテストを追加する。
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
    )
    # TODO(p3): 投稿に紐づくコメントの標準の並び順をモデル側で扱うか検討する。


# TODO(p2): コメントにも更新日時を追加し、編集機能を作る準備をする。frontend 影響あり。
class Comment(Base):
    __tablename__ = "comments"

    # TODO(p3): 主キーに対する index=True の必要性を投稿テーブルと同じ観点で整理する。
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # TODO(p2): 存在しない投稿IDにコメントを作れないことをDB制約とAPIで確認するテストを追加する。
    # TODO(p2): コメント本文の空文字禁止や長さの上限をDB側でも表現する。
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # TODO(p3): コメント一覧を作成日時で並べる処理に合うインデックスを検討する。
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    post: Mapped[Post] = relationship(back_populates="comments")
    # TODO(p2): 投稿削除時にコメントも削除されることを確認するテストを追加する。
