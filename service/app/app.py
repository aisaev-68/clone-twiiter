from typing import List
import asyncio
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from pathlib import Path

from fastapi import FastAPI, status, Form, Depends, \
    HTTPException, File, UploadFile, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from werkzeug.utils import secure_filename
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm.session import Session
from database import engine, Base, session
from schemas import TweetOut, ImageOut, TweetIn, AuthModel, DefaultError, Token
from models import User, Tweet
from utils import allowed_file, add_image
from auth import authenticate
from crypt import create_token_jwt, get_password_hash
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
security = HTTPBasic()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    new_user = User(username="kaanersoy",
                    hashed_password=get_password_hash("password"),
                    email="asd@ya.ru")

    async with session.begin():
        session.add(new_user)
    # access_token = create_token_jwt(new_user)
    # print(access_token)


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


@app.post(path='/login',
          response_model=Token,
          status_code=status.HTTP_200_OK,
          summary="Login a user",
          responses={401: {"model": DefaultError}},
          )
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    api_token = create_token_jwt(user)
    print(111111, api_token)

    response.set_cookie(
        key="api_token",
        value=f"Bearer {api_token}",
        httponly=True
    )
    return {"api_token": api_token, "token_type": "bearer"}



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