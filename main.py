from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import Response
from typing import Optional

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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



@app.get('/posts')
async def get_posts():
    return {'data': my_posts}


# Get the user - payload
# @app.post('/createposts')
# async def create_posts(payload: dict = Body(...)):
#     print('---payload---', payload, '\n', Body(...))
#     return {"new_post": f'Title: {payload['title']}\nContent: {payload['content']}'}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 10000)
    my_posts.append(post.model_dump())
    return {'data': post_dict}


@app.get('/posts/latest')
async def get_latest_post():
    post = my_posts[len(my_posts)-1]

    return {'data': post}


# path parameter
@app.get('/posts/{id}')
async def get_post(id: str, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'Post id not found!'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found!"
        )
    return {'detail': post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str):
    index = find_index_post(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    my_posts.pop(index)

    return {'message': 'Post was successfully deleted!'}


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: str, payload: Post):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    print(payload)
    return {'message': 'Updated post'}


# 2:18