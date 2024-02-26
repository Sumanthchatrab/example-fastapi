from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, utils, oauth

router = APIRouter(tags=['Auth'])

@router.post("/login", response_model= schema.Token)
def userlogin(credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify_pass(credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth.create_token(data= {"user_id" : user.id})

    return {"access_token": access_token, "token_type": "Bearer"}





    