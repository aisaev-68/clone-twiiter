from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
import jwt
from settings import ALGORITHM, SECRET_KEY, TTL_JWT


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')



class Auth():
    hasher = CryptContext(schemes=['bcrypt'], deprecated="auto")
    secret = SECRET_KEY

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def create_jwt_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=int(TTL_JWT)),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=ALGORITHM
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=ALGORITHM)
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=int(TTL_JWT)),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=ALGORITHM
        )

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'refresh_token'):
                username = payload['sub']
                new_token = self.create_jwt_token(username)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')
