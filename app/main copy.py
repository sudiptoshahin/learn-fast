from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import Response
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {'status': "Success"}



# @app.get('/posts')
# async def get_posts():
#     return {'data': my_posts}

@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute(
            """
            INSERT INTO posts (title, content, published) 
            VALUES (%s, %s, %s) 
            RETURNING *;
            """,
            (post.title, post.content, post.published)
        )
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


@app.get('/posts/latest')
async def get_latest_post():
    post = my_posts[len(my_posts)-1]

    return {'data': post}


# path parameter
# @app.get('/posts/{id}')
# async def get_post(id: str, response: Response):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {id} was not found!"
#         )
#     return {'detail': post}
@app.get('/posts/{id}')
async def get_post(id: str, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id))
    test_post = cursor.fetchone()
    post = find_post(id)
    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} was not found!"
    #     )
    return {'detail': test_post}


# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: str):
#     index = find_index_post(id)
#     if not index:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Post not found'
#         )
#     my_posts.pop(index)

#     return {'message': 'Post was successfully deleted!'}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id))
    delete_post = cursor.fetchone()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: str, post: Post):

    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )

    return {'message': updated_post}


# 2:18