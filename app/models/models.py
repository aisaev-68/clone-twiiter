from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)

from sqlalchemy.orm import relationship, backref

from db.database import Base

likes = Table("likes",
              Base.metadata,
              Column("user_id", Integer, ForeignKey("user.id")),
              Column("post_id", Integer, ForeignKey("post.id")),
              )

followers = Table('follows',
                  Base.metadata,
                  Column('follower_id', Integer,
                         ForeignKey('user.id'), nullable=True),
                  Column('followed_id', Integer,
                         ForeignKey('user.id'), nullable=True)
                  )


class User(Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(25), unique=True, nullable=False)
    api_token: str = Column(Text(), nullable=False)
    posts: List["Post"] = relationship("Post",
                                       back_populates="author",
                                       lazy="selectin",
                                       cascade="all, delete, delete-orphan")

    likes = relationship(
        "Post", secondary=likes,
        backref=backref("likes", lazy="dynamic"),
        lazy="dynamic",
        cascade="all, delete",
    )

    following: List["User"] = relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates="followers",
        lazy="selectin",
    )
    followers: List["User"] = relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates="following",
        lazy="selectin",
    )

    def __repr__(self):
        return f"User"

    def to_json(self) -> Dict[str, Any]:
        print(55555, self.id, self.username, self.followers)
        return {
            'id': self.id,
            'name': self.username,
            'followers': [
                {'id': user.id, 'name': user.username}
                for user in self.followers
            ],
            'following': [
                {'id': user.id, 'name': user.username}
                for user in self.following
            ],
        }


class Post(Base):
    __tablename__ = "post"
    id: int = Column(Integer, primary_key=True)
    content: str = Column(Text, nullable=False)
    date_posted: datetime = Column(DateTime, default=datetime.now)
    user_id: int = Column(Integer, ForeignKey('user.id'), nullable=False)
    author: Optional[User] = relationship("User", back_populates="posts", lazy=True)
    post_image: List["Media"] = relationship("Media", back_populates="medias", lazy="selectin",
                                             cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Post ({self.id}', '{self.content}', '{self.date_posted}')"

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "author": {
                "id": self.author.id,
                "name": self.author.username,
            },
            "attachments": [image.to_json()["url"] for image in self.post_image],
            "likes": [
                {"user_id": like.user_id, "name": self.author.username}
                for like in self.author.likes
            ],
        }


class Media(Base):
    __tablename__ = "media"
    id: int = Column(Integer, primary_key=True)
    post_id: int = Column(Integer, ForeignKey("post.id"))
    path_file: str = Column(Text(), nullable=False)
    medias: List["Post"] = relationship("Post", back_populates="post_image", lazy=True)

    def __repr__(self):
        return f"Media ({self.id}', '{self.post_idt}', '{self.path_file}')"

    def to_json(self) -> Dict[str, Any]:
        return {
            "url": self.path_file
        }
