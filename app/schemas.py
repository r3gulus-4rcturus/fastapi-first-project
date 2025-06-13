from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


# Pydantic Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default = True, jadi kalo user ga specify published, published akan bernilai true

class PostCreate(PostBase):
    pass

# hanya untuk handle create user
class UserCreate(BaseModel):
    email: EmailStr # untuk validasi alamat email
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
# misalkan untuk update Post, user hanya boleh
# mengupdate field published aja (title sm content gabole diubah)
# kita bisa melakukan pembatasan seperti itu dengan hanya menyediakan
# field published pada UpdatePost
class PostUpdate(BaseModel):
    published: bool = True  # default = True, jadi kalo user ga specify published, published akan bernilai true
 
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # Agar kita bisa melakukan mereturn sqlalchemy model dalam bentuk model ini  
    # jadi nantinya sqlalachemy model akan otomatis diconvert menjadi pydantic model ini sebelum direturn sebagai response
    class Config:
        orm_mode = True

class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int

    # Agar kita bisa melakukan mereturn sqlalchemy model dalam bentuk model ini  
    # jadi nantinya sqlalachemy model akan otomatis diconvert menjadi pydantic model ini sebelum direturn sebagai response
    class Config:
        orm_mode = True



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   # untuk validasi integer yg disimpan harus less than equal 1



