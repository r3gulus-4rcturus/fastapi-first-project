from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils   # untuk specify file di directory sebelumnya, tambahkan ..                     # untuk mengakses semua model yg udah kita buat (models.Post, ...)
from ..database import get_db

# pengganti FastAPI object yg ada di main
# Kalo kita memakai konsep router (path operation dipecah menjadi beberapa file)
# instance API yg digunakan adalah APIRouter
router = APIRouter(
    prefix="/users",
    tags=['Users']
)    

# adapun untuk decorator path operation, pake @router (klo instance FastAPI di main pakenya @app)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)    
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password (from user.password)
    hashed_pwd = utils.hash(user.password)
    # save it back to the pydantic model
    user.password = hashed_pwd
    
    new_user = models.User(**user.dict())      
    db.add(new_user)     
    db.commit()           
    db.refresh(new_user)   

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)    
def get_user(id: int, db: Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

    return user
