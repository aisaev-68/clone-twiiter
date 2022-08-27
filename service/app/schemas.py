from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class TweetOut(BaseModel):
    result: bool = True
    tweet_id: int

    class Config:
        orm_mode = True


class TweetIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=250, example="My first tweet!")


class ImageOut(BaseModel):
    id: List[int]

    class Config:
        orm_mode = True


class DefaultError(BaseModel):
    result: bool = False
    error_type: str
    error_message: str

class AuthModel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    # token_type: str
