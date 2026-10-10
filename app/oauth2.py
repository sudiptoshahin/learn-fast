
from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# Algorithm
# Expiration Time

# Generate secret key: `openssl rand -hex 32``
SECRET_KEY = '222c8862dae8c450dbdbce28c6b6b5ca000d9c36a57b2f8f464c108463dd46cf'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUITES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUITES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
