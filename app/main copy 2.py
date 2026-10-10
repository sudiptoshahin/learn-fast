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


# ===== Path Operation ================
@app.get('/')
async def root():
    return {'message': 'Hello world. Welcome to my API'}


@app.get('/posts', status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
async def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session=Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get('/posts/latest')
async def get_latest_post():
    post = my_posts[len(my_posts)-1]

    return {'data': post}


@app.get('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def get_post(id: str, response: Response, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found!"
        )
    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: str, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_obj = post_query.first()
    
    if not post_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # has the password - user.password
    hash_pwd = hash_password(user.password)
    user.password = hash_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(id: str, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found!"
        )

    return user




# 6:12 