from .. import models, schema, utils, oauth
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional


router= APIRouter(
    prefix="/alchemy",
    tags=['Posts']
)

@router.get("/", response_model=List[schema.respost],)
def testpost(db: Session = Depends(get_db),user: int = Depends(oauth.get_current_user),
             limit : int =5, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    return posts

@router.get("/{id}",response_model=schema.respost)  
def getbyids(id: int,db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id==id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schema.respost)
def createpost(newdata: schema.postschema ,db: Session = Depends(get_db),
                user: int = Depends(oauth.get_current_user)):
    #newpost = models.Post(title=newdata.title,content=newdata.content)

    newpost = models.Post(owner_id=user.id,**newdata.dict())
    print(type(newpost))
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost

@router.delete("/{id}")
def deletepost(id:int,db: Session = Depends(get_db),
        user: int = Depends(oauth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    if user.id==post.first().owner_id:
        post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schema.respost)
def updatepost(newdata: schema.putscehma, id : int, db: Session = Depends(get_db)):
    postquery= db.query(models.Post).filter(models.Post.id == id)
    if not postquery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    postquery.update(newdata.dict(), synchronize_session= False)
    db.commit()
    print(postquery)
    return postquery.first()

