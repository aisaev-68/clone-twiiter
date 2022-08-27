from datetime import datetime, timedelta
from os import environ

from jose import jwt
from passlib.context import CryptContext

from models import User
from settings import ALGORITHM, SECRET_KEY, TTL_JWT


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def create_token_jwt(user: User, extra_fields={}):
    ttl = int(TTL_JWT)
    data = {
        'exp': datetime.utcnow() + timedelta(minutes=ttl),
        'id': user.id,
        'username': user.username,
    }

    data.update(extra_fields)

    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token


def decode_token_jwt(token: str):
    data = jwt.decode(token, SECRET_KEY, ALGORITHM)
    return data


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)