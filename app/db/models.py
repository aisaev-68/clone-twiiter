from datetime import datetime
from typing import Any, Dict, List, Optional

from db.database import Base
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import backref, relationship


class User(Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(25), unique=True, nullable=False)
    api_token: str = Column(Text(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tweets: List["Tweet"] = relationship(
        "Tweet",
        back_populates="user",
        cascade="all, delete, delete-orphan"
    )


    followers: List["Follows"] = relationship(
        "User",
        secondary="followings",
        primaryjoin="User.id == Follows.user_id",
        secondaryjoin="User.id == Follows.follows_user_id",
        back_populates="follows",
        lazy="selectin",
        uselist=True,
    )
    follows: List["Follows"] = relationship(
        "User",
        secondary="followings",
        primaryjoin="User.id == Follows.follows_user_id",
        secondaryjoin="User.id == Follows.user_id",
        back_populates="followers",
        lazy="selectin",
        uselist=True,
    )
    tweet_likes = relationship("TweetLikes", back_populates="user")

    def __repr__(self):
        return f"User ('{self.username}')"

    def to_json(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.username,
            'following': [
                {
                    "id": followers.id,
                    "name": followers.username
                }
                for followers in self.followers
            ],
            'followers': [
                {
                    "id": follows.id,
                    "name": follows.username
                }
                for follows in self.follows
            ],
        }


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"))

    user: Optional["User"] = relationship("User", back_populates="tweets",
                                          foreign_keys=[user_id])
    likes: List["TweetLikes"] = relationship("TweetLikes", back_populates="tweet")

    tweet_image: List["Media"] = relationship("Media", back_populates="medias")

    def __repr__(self):
        return f"Tweet ({self.id}', '{self.content}', '{self.created_at}')"

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "author": {
                "id": self.user.id,
                "name": self.user.username,
            },
            "attachments": [image.to_json()["url"] for image in self.tweet_image],
            "likes": [
                like.to_json() for like in self.likes
            ],
        }


class Follows(Base):
    """<user_id> follows <follows_user_id>
    """
    __tablename__ = "followings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    follows_user_id = Column(Integer, ForeignKey("user.id"))

    # user: Optional["User"] = relationship("User", back_populates="follows",
    #                                       foreign_keys=[user_id])
    # follows_user: Optional["User"] = relationship(
    #     "User", back_populates="followers", foreign_keys=[follows_user_id])



class TweetLikes(Base):
    __tablename__ = "tweet_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    tweet_id = Column(Integer, ForeignKey("tweet.id"))

    # user = relationship("User", back_populates="tweet_likes",
    #                     foreign_keys=[user_id])
    # tweet = relationship("Tweet", back_populates="likes",
    #                      foreign_keys=[tweet_id])
    user = relationship("User", back_populates="tweet_likes")
    tweet = relationship("Tweet", back_populates="likes")

    def to_json(self):
        return {"user_id": self.user.id,
                "name": self.user.username}


class Media(Base):
    __tablename__ = "media"
    id: int = Column(Integer, primary_key=True)
    tweet_id: int = Column(Integer, ForeignKey("tweet.id"))
    path_file: str = Column(Text(), nullable=False)
    medias: Optional["Tweet"] = relationship("Tweet", back_populates="tweet_image")

    def __repr__(self):
        return f"Media ({self.id}', '{self.tweet_id}', '{self.path_file}')"

    def to_json(self) -> Dict[str, Any]:
        return {
            "url": self.path_file
        }
