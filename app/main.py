from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import get_logger
from routers import likes, medias, tweets, users
from db.schemas import Failure

logger = get_logger("main")


def get_application() -> FastAPI:
    application = FastAPI(
        title="Clone-tweeter",
        description="Итоговый проект по курсу Python advanced. Skiilbox.",
        version="0.1.0",
        responses={
            422: {
                "description": "Ошибка проверки",
                "model": Failure,
            },
        },
    )

    application.include_router(users.router)
    application.include_router(tweets.router)
    application.include_router(medias.router)
    application.include_router(likes.router)

    origins = [
        "http://localhost:8080",
        "http://0.0.0.0:8080",
        "http://127.0.0.1:8080",
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
