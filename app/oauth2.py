# Handling JWT

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .config import settings

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# We need to provide 3 things
# (1) SECRET KEY
# (2) Algorithm 
# (3) Expiration Time

# ini sebenernya   bad practice, SECRET KEY TIDAK BOLEH HARDCODED
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    # provide the time limit that is going to expire
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt  

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

# ini kita ngebikin dependency buat endpoint2 yg ada di post/user
# Jadi, untuk semua path operation di aplikasi ini yang mengharuskan 
# user untuk LOGIN (contoh: ngepost postingan baru, update postingan, itu kan harus login)
# kita bakal nambain dependency ini (get_current_user) di path operation itu
# kenapa ga langsung pake verify access token aja? dengan get_current_user, kita bisa sekaligus
# ngefetch data user dari database, yg nantinya bisa kita gunakan pada path operation. 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # fetch user data from the database
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user
