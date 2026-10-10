from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from fastapi import Response
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app import schemas
from passlib.context import CryptContext
from app.utils.security import hash_password, verify_password
from app.routers import user, post, auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


#==============Database connection====================
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='learn-fastapi', user='sudipto', password='shahin123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(f"Database connection was successful!")
        break
    except Exception as err:
        print(f'Something went wrong. Errror: {err}')

#==============================================


my_posts = [
    {'id': '123', 'title': "Title post 1", 'content': 'Content post 1'},
    {'id': '124', 'title': "Title post 2", 'content': 'Content post 2'},
    {'id': '125', 'title': "Title post 3", 'content': 'Content post 3'},
]

def find_post(id: str):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None


def find_index_post(id: str):
    for idx, post in enumerate(my_posts):
        if post['id'] == id:
            return idx
    return None


# ===== Attach rotuers to the app =========
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


# ======================================= #


# ===== Path Operation ================
@app.get('/')
async def root():
    return {'message': 'Hello world. Welcome to my API'}






# 07:14