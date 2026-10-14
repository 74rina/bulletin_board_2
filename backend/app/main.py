from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

# TODO(p3): API名やバージョンをOpenAPIに表示し、ドキュメントから用途が分かるようにする。
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # TODO(p1): CORSの許可オリジンをREADMEやdocker-composeのポートと揃える。frontend 影響あり。
    allow_origins=["http://localhost:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    # TODO(p2): 稼働確認用のエンドポイントでDB接続状態も確認できるようにする。
    return {"message": "Hello FastAPI"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # TODO(p2): リクエスト処理中にDBエラーが起きたときにロールバックされることを確認できるテストを追加する。
        db.close()


@app.post("/posts", response_model=schemas.PostListItem)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    # TODO(p1): 投稿作成時に空白だけの名前・タイトル・本文を受け付けないようにする。
    post = models.Post(name=payload.name, title=payload.title, body=payload.body)
    db.add(post)
    db.commit()
    db.refresh(post)
    # TODO(p3): 投稿作成レスポンスの組み立てを共通化し、レスポンスモデルの変換を学べるようにする。
    return schemas.PostListItem(
        id=post.id,
        name=post.name,
        title=post.title,
        body=post.body,
        created_at=post.created_at,
        comment_count=0,
    )


@app.get("/posts", response_model=list[schemas.PostListItem])
def list_posts(db: Session = Depends(get_db)):
    # TODO(p2): 投稿一覧にページネーションを追加し、大量データでも一定件数ずつ返せるようにする。frontend 影響あり。
    # TODO(p3): 投稿一覧でタイトルや本文を検索できる条件を追加する。frontend 影響あり。
    rows = (
        db.query(models.Post, func.count(models.Comment.id).label("comment_count"))
        .outerjoin(models.Comment, models.Comment.post_id == models.Post.id)
        .group_by(models.Post.id)
        # TODO(p2): 同じ作成日時の投稿でも一覧順が安定するように並び順を見直す。
        .order_by(models.Post.created_at.desc())
        .all()
    )
    # TODO(p2): コメント数の集計結果が正しいことを確認するAPIテストを追加する。
    return [
        schemas.PostListItem(
            id=post.id,
            name=post.name,
            title=post.title,
            body=post.body,
            created_at=post.created_at,
            comment_count=comment_count,
        )
        for post, comment_count in rows
    ]


@app.get("/posts/{post_id}", response_model=schemas.PostDetail)
def get_post(post_id: int, db: Session = Depends(get_db)):
    # TODO(p3): post_id が0以下のときのエラーレスポンスを分かりやすくする。
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        # TODO(p3): 404エラーのdetail文言を日本語にするか英語にするかAPI全体で統一する。frontend 影響あり。
        raise HTTPException(status_code=404, detail="Post not found")
    # TODO(p3): 投稿詳細のコメント一覧にも件数制限を追加する。frontend 影響あり。
    comments = (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .order_by(models.Comment.created_at.asc())
        .all()
    )
    return schemas.PostDetail(
        id=post.id,
        name=post.name,
        title=post.title,
        body=post.body,
        created_at=post.created_at,
        comments=comments,
    )


@app.post("/posts/{post_id}/comments", response_model=schemas.CommentOut)
def create_comment(
    post_id: int,
    payload: schemas.CommentCreate,
    db: Session = Depends(get_db),
):
    # TODO(p1): コメント作成時に空白だけの本文を受け付けないようにする。
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = models.Comment(post_id=post_id, body=payload.body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    # TODO(p2): コメント作成後のレスポンスに post_id を含め、クライアントが更新対象を判断しやすくする。frontend 影響あり。
    return comment


# TODO(p2): 投稿を編集するAPIを追加し、HTTP PUT/PATCHの使い分けを学べるようにする。frontend 影響あり。
# TODO(p2): 投稿を削除するAPIを追加し、コメントとの削除関係を確認できるようにする。frontend 影響あり。
# TODO(p2): コメントを削除するAPIを追加し、子リソースの扱いを学べるようにする。frontend 影響あり。
