# Post Router

from app import models, schemas
from app.database import get_db
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
async def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session=Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @router.get('/posts/latest')
# async def get_latest_post():
#     post = my_posts[len(my_posts)-1]

#     return {'data': post}


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def get_post(id: str, response: Response, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found!"
        )
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
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