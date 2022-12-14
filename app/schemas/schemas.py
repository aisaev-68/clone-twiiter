from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    id: int
    name: str


class LikeUser(BaseModel):
    user_id: int
    name: str


class FollowModel(BaseUser):
    followers: Optional[list[BaseUser]]
    following: Optional[list[BaseUser]]


class UserOut(BaseModel):
    result: bool = True
    user: FollowModel


class ApiToken(BaseModel):
    api_token: str


class TweetsResponseModel(BaseModel):
    id: int
    content: str
    timestamp: str
    attachments: Optional[list[str]]
    author: BaseUser
    likes: Optional[list[LikeUser]]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int]


class NewTweetOut(BaseModel):
    result: bool = True
    tweet_id: int

    class Config:
        orm_mode = True


class TweetsOut(BaseModel):
    result: bool
    tweets: list[TweetsResponseModel]


class Success(BaseModel):
    result: bool = True


class FileSuccess(Success):
    media_id: int


class TweetSuccess(Success):
    tweet_id: int


class Failure(Success):
    error_type: str
    error_message: str
