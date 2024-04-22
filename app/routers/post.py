from app import oauth2
from .. import models, schemas 
from typing import List, Optional
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends, status, Response, HTTPException, APIRouter

router = APIRouter(
        prefix='/posts',
        tags=['Posts']
        )

# @router.get("/", status_code=status.HTTP_200_OK)
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post_w_Vote])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = (
        db.query(models.Posts, func.count(models.Vote.post_id).label('total_votes'))
            .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
            .group_by(models.Posts.id)
            .filter(models.Posts.title.contains(search))
            .offset(skip)
            .limit(limit)
            .all()
    )
    return posts

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post_w_Vote)
def get_post(id: int, db: Session = Depends(get_db)):
    post = (
        db.query(models.Posts, func.count(models.Vote.post_id)
            .label('total_votes'))
            .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
            .group_by(models.Posts.id)
            .filter(models.Posts.id == id)
            .first()
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} was not found!")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Posts(**post.model_dump(), user_id=current_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    print(post_query.first())

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} doesn't exist!")

    if post_query.first().user_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} doesn't exist!")
    if post_query.first().user_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post

