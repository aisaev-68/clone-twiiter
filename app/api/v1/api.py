from fastapi import APIRouter

from app.api.v1.endpoints import media, tweet, user

api_router = APIRouter()
api_router.include_router(user.router, tags=["Users"])
api_router.include_router(tweet.router, prefix="/api/tweets", tags=["Tweets"])
api_router.include_router(media.router, prefix="/api/medias", tags=["Tweets"])