from datetime import datetime
from typing import List

from pydantic import BaseModel


class PostCreate(BaseModel):
    name: str
    title: str
    body: str


class CommentCreate(BaseModel):
    body: str


class CommentOut(BaseModel):
    id: int
    body: str
    created_at: datetime

    class Config:
        from_attributes = True


class PostListItem(BaseModel):
    id: int
    name: str
    title: str
    body: str
    created_at: datetime
    comment_count: int

    class Config:
        from_attributes = True


class PostDetail(BaseModel):
    id: int
    name: str
    title: str
    body: str
    created_at: datetime
    comments: List[CommentOut]

    class Config:
        from_attributes = True
