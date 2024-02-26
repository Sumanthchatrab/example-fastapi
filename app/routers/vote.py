from fastapi import status, HTTPException, Depends, APIRouter
from .. import schema, database, models, oauth
from sqlalchemy.orm import Session

router= APIRouter(
    prefix= "/vote",
    tags= ['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Votes, db : Session = Depends(database.get_db), user: int = Depends(oauth.get_current_user)):
    vote_query = db.query(models.votes).filter(models.votes.post_id==vote.post_id, models.votes.user_id==user.id)
    found_vote = vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f" user {user.id} has already voted for post {vote.post_id}")
        new_vote = models.votes(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Voted succesfuly"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
        vote_query.delete()
        db.commit()
        return {"message":"Succesfully deleted vote"}
    
  

    

