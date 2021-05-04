from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger, Text, Table

from .mixins import IdMixin, UrlMixin


Base = declarative_base()

tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Post(Base, UrlMixin):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False, unique=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=True)
    author = relationship("Author", backref="posts")
    tags = relationship("Tag", secondary=tag_post)


class Author(Base, UrlMixin):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


class Tag(Base, UrlMixin):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    body = Column(String)
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship(Post, backref="comments")

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.parent_id = kwargs["parent_id"]
        self.body = kwargs["body"]
