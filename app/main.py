from core.app_events import create_start_app_handler, create_stop_app_handler
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from logger.logger import get_logger
from routers import likes, medias, tweets, users
from schemas.schemas import Failure
from starlette.templating import _TemplateResponse as TemplateResponse

logger = get_logger("main")

templates = Jinja2Templates(directory="static")


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
    })
    application.mount("/static", StaticFiles(directory="static"), name="static")
    application.mount("/images", StaticFiles(directory="images"), name="images")

    application.add_event_handler("startup", create_start_app_handler())
    application.add_event_handler("shutdown", create_stop_app_handler())

    application.include_router(users.router)
    application.include_router(tweets.router)
    application.include_router(medias.router)
    application.include_router(likes.router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return application


app = get_application()


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def home(req: Request) -> TemplateResponse:
    """
    Маршрут перехода на главную страницу.

    :param req:
    :return:
    """
    logger.info("Переход на главную страницу.")
    return templates.TemplateResponse("index.html", {"request": req})