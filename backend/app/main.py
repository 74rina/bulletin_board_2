from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/posts", response_model=schemas.PostListItem)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(name=payload.name, title=payload.title, body=payload.body)
    db.add(post)
    db.commit()
    db.refresh(post)
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
    rows = (
        db.query(models.Post, func.count(models.Comment.id).label("comment_count"))
        .outerjoin(models.Comment, models.Comment.post_id == models.Post.id)
        .group_by(models.Post.id)
        .order_by(models.Post.created_at.desc())
        .all()
    )
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
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
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
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = models.Comment(post_id=post_id, body=payload.body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
