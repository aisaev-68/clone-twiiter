from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from database import session, engine
from models import User
from crypt import decode_token_jwt, pwd_context

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token_jwt(token)
        del payload['exp']
        return payload
    except:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        raise credentials_exception


async def authenticate(username: str, password: str):
    stmt_user = select(User).where(User.username == username)

    user = await session.execute(stmt_user)
    user = user.scalar()

    if not user:
        return False

    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user



