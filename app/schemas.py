from typing import Optional, Tuple
from pydantic import BaseModel, ConfigDict, EmailStr, Field
import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime.datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime.datetime 
    user_id: int
    user: UserOut

class Post_w_Vote(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Posts: PostResponse
    total_votes: int

class Vote(BaseModel):
    post_id: int
    dir: int = Field(le=1, ge=0)
