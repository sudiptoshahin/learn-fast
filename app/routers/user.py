# User Router

from app import models, schemas
from app.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.utils.security import hash_password, verify_password


router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # has the password - user.password
    hash_pwd = hash_password(user.password)
    user.password = hash_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(id: str, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found!"
        )

    return user