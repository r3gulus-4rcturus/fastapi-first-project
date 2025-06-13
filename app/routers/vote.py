from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2   # untuk specify file di directory sebelumnya, tambahkan ..                     # untuk mengakses semua model yg udah kita buat (models.Post, ...)
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), 
         current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    # periksa apakah post_id valid
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exist")

    # vote.dir = 1 vote, 0 unvote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    # vote
    if (vote.dir == 1):
        # periksa apakah sebelumnya udah ngevote, kalo udah gaboleh ngevote lagi
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    
    # unvote
    else :
        # periksa apakah sebelumnya udah ngevote, kalo belom ya gmn kita bisa unvote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
