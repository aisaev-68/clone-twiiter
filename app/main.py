from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schema.schemas import Failure
from app.api.v1.api import api_router as api_router_v1
from app.utils.logger import get_logger

logger = get_logger("main")

app = FastAPI(
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



origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router_v1)
