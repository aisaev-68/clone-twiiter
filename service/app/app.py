from typing import List
import asyncio
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from pathlib import Path
from sqlalchemy import select
from fastapi import FastAPI, status, Form, Depends, \
    HTTPException, File, UploadFile, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from werkzeug.utils import secure_filename
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm.session import Session
from database import engine, Base, session
from schemas import TweetOut, ImageOut, TweetIn, AuthModel, DefaultError, Token
from models import User, Tweet
from utils import allowed_file, add_image
from auth import Auth
from forms import LoginForm


app = FastAPI(
    title="Twitter API",
    description="This is a copy of Twitter API",
    version="1.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Users Routes",
        },
        {
            "name": "Tweets",
            "description": "Tweets Routes",
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(HTTPSRedirectMiddleware)
security = HTTPBearer()
auth_handler = Auth()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    new_user = User(username="kaanersoy",
                    hashed_password=auth_handler.encode_password("password"),
                    email="asd@ya.ru")

    async with session.begin():
        session.add(new_user)

    print(new_user.hashed_password)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/")
def root():
    """ Root GET """
    return RedirectResponse("/login")


@app.get('/login')
async def login_redirect(request: Request):
    return templates.TemplateResponse("index.html", {"request": request},)


@app.post('/login',
          response_model=Token,
          status_code=status.HTTP_200_OK,
          summary="Login a user",
          responses={401: {"model": DefaultError}},
          )
async def login(user_details: AuthModel):

    stmt_user = select(User).where(User.username == user_details.username)

    user = await session.execute(stmt_user)
    user = user.scalar()
    print(11111, user)

    if user is None:
        return HTTPException(status_code=401, detail='Invalid username')

    if not auth_handler.verify_password(user_details.password, user.hashed_password):
        return HTTPException(status_code=401, detail='Invalid password')

    access_token = auth_handler.create_jwt_token(user.username)
    refresh_token = auth_handler.encode_refresh_token(user.username)
    return {'access_token': access_token, 'refresh_token': refresh_token}




# @app.post(
#     path="/api/tweets",
#     response_model=TweetOut,
#     status_code=status.HTTP_201_CREATED,
#     summary="Post a tweet",
# )
# async def post_tweet(tweet: TweetIn, user: User):
#     new_tweet = await Tweet(content=tweet.content, user=user)
#     session.add(new_tweet)
#     await session.commit()
#     await session.refresh(new_tweet)
#     return new_tweet
#
#
# @app.post(path="/api/media",
#           response_model=ImageOut,
#           status_code=status.HTTP_201_CREATED,
#           summary="Post a images"
#           )
# async def uploads_image(files: List[UploadFile] = File(...)) -> List[int]:
#     id_image_list = []
#     file_list = [file.filename for file in files]
#     for file in file_list:
#         if file and allowed_file(file):
#             filename = secure_filename(file)
#             async with aiofiles.open(filename, "wb") as buffer:
#                 data = await buffer.read()
#             id_image = await add_image(session, filename, data)
#             id_image_list.append(id_image)
#     return id_image_list

# if __name__ == "__main__":
#     uvicorn.run(
#         app="app:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )