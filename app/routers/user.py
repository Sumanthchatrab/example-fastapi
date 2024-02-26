from .. import models, schema, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/user",tags=['Users']
)

@router.post("/",response_model=schema.userout, status_code=status.HTTP_201_CREATED)
def adduser(user: schema.user,  db: Session = Depends(get_db)):
    #hashing password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    userdata = models.User(**user.dict())
    db.add(userdata)
    db.commit()
    db.refresh(userdata)
    return userdata

@router.get("/{id}", response_model=schema.userout)
def getuser(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user