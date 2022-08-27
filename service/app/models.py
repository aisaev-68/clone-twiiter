from typing import Any

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, \
    ForeignKey, ARRAY, Table, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    username = Column(String(256), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    birth_date = Column(Date, nullable=True)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    tweets = relationship(
        "Tweet", foreign_keys="[Tweet.user_id]", back_populates="user"
    )
    following = relationship(
        "User",
        lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        lazy="dynamic",
    )
    followers = relationship(
        "User",
        lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.following_id,
        secondaryjoin=lambda: User.id == user_following.c.user_id,
        lazy="dynamic", overlaps="following",
    )

    liked_tweets = relationship(
        "Tweet",
        lambda: user_like_tweet,
        primaryjoin=lambda: User.id == user_like_tweet.c.user_id,
        secondaryjoin=lambda: Tweet.id == user_like_tweet.c.tweet_id,
        lazy="dynamic",
        backref="likes",
    )

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()



user_like_tweet = Table(
    "user_like_tweet",
    Base.metadata,
    Column("is_active", Boolean(), default=True),
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("tweet_id", Integer, ForeignKey("tweet.id"), primary_key=True),
)


user_following = Table(
    "user_following",
    Base.metadata,
    Column("is_active", Boolean(), default=True),
    Column("user_id", Integer, ForeignKey(User.id), primary_key=True),
    Column("following_id", Integer, ForeignKey(User.id), primary_key=True),
)

class Tweet(Base):
    __tablename__ = "tweet"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    content = Column(String(250), nullable=False)
    id_image = Column(ARRAY(item_type=Integer, as_tuple=True))
    is_active = Column(Boolean(), default=True)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id], back_populates="tweets")

    @property
    def likes_count(self):
        return len(self.likes)


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    img_filename = Column(String())
    img_data = Column(LargeBinary)

# {id: "", username: "", password: "", profile: {pic: "", nickname: "", name: ""}}