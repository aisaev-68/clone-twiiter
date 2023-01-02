from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(25), unique=True, nullable=False)
    api_token: str = Column(Text(), nullable=False)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())

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
        return "{name}, ({id}, username})".format(
            name=self.__class__.__name__,
            id=self.id,
            username=self.username
        )

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

    id: int = Column(Integer, primary_key=True, index=True)
    content: str = Column(String, index=True)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    user_id: int = Column(Integer, ForeignKey("user.id"))

    user: Optional["User"] = relationship("User", back_populates="tweets")
    likes: List["TweetLikes"] = relationship("TweetLikes", back_populates="tweet")

    tweet_image: List["Media"] = relationship("Media", back_populates="medias")

    def __repr__(self):
        return "{name} ({id}, {content}, {date_create})".format(
            name=self.__class__.__name__,
            id=self.id,
            content=self.content,
            date_create=self.created_at
        )

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

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    follows_user_id: int = Column(Integer, ForeignKey("user.id"))


class TweetLikes(Base):
    __tablename__ = "tweet_likes"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    tweet_id: int = Column(Integer, ForeignKey("tweet.id"))

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
        return "{name} ({id}', '{tweet_id}', '{path_file}')".format(
            name=self.__class__.__name__,
            id=self.id,
            tweet_id=self.tweet_id,
            path_file=self.path_file
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "url": self.path_file
        }
