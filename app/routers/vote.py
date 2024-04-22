from fastapi import Depends, status, Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db

from .. import schemas, oauth2, models

router = APIRouter(
    prefix='/votes',
    tags = ['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def make_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(vote.post_id)
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id: {vote.post_id} was not found.')
    vote_in_db_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user)
    if (vote.dir == 1):
        if vote_in_db_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'The user with id: {current_user} has already voted the post with id: {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote."}
    if (vote.dir == 0):
        if not vote_in_db_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist.')
        vote_in_db_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote."}
