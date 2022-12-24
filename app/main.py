from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import get_logger
from routers import tweet, user, media, like
from db.schemas import Failure

logger = get_logger("main")


def get_application() -> FastAPI:
    application = FastAPI(
        title="Clone-tweeter",
        description="Итоговый проект по курсу Python advanced. Skiilbox.",
        version="0.1.0",
        docs_url="/api/docs",
        responses={
            422: {
                "description": "Ошибка проверки",
                "model": Failure,
            },
        },
    )

    application.include_router(user.router)
    application.include_router(tweet.router)
    application.include_router(media.router)
    application.include_router(like.router)

    origins = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://0.0.0.0:8080",
        "http://localhost",
        "http://127.0.0.1",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return application


app = get_application()
