
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models, oauth2
from app.utils.security import hash_password, verify_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm = {
    #   'username': '......',
    #    'password': '......'
    # }
    #

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid credentials'
        )

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}
    

