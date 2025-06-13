# JWT AUTHENTICATION (JSON WEB TOKEN)
# gimana cara kita ngetrack apakah user saat ini sedang logged in atau tidak?
# cara 1: bikin state yang nyimpen apakah user sedang login/catet waktu kapan dia log in untuk tiap data User
# cara 2: JWT AUTHENTICATiON. Stateless (gaperlu nyimpen data di database seperti cara 1)
#         Idenya adalah, informasi apakah user log in atau tidak disimpan di frontend/client (bukan database/api/backend)
# Gimana cara kerjanya:
# Pertama, client akan melakukan request berupa login dengan menyertakan username dan password
# API akan ngecek passwordnya sama atau enggak, kalo enggak ditolak, kalo sama client bakal dikasih TOKEN
# Token ini adalah suatu string (kaya gibberish gitu) yang terdiri dari: 
# (1) HEADER (nyimpen tipe algoritma)
# (2) PAYLOAD (nyimpen data username, dan id) [JANGAN NYIMPEN PASSWORD DISINI]
# (3) SIGNATURE (Hasil encoding base 64 dari HEADER + PAYLOAD + SECRET)
#  [Perhatikan bahwa TOKENNYA sendiri ini bisa dilihat/gak encrypted, jadi jangan menyertakan password di dalam token]
#  Nah jadi, token ini akan dikirim ke client, dimana nanti saat client melakukan request
# yang memerlukan autentikasi, ia harus menyertakan token ini kepada API (semacam tanda pengenal kalo kamu udh terautentikasi)
# Jadi, saat melakukan request, API akan melakukan pencocokan antara SECRET yg ia simpan dengan SECRET yg dikirimkan di 
# token yg dikirimkan bebarengan dengan request tadi
# Hacker ga bakal bisa ngeleak data seseorang dengan hanya mengganti id nya yg ada di payload, karena tetap ada yg namanya SECRET
# Dimana itu hanya diketahui oleh user dan API. 

# cara decode token: ke jwt.io (kalo pengen tau informasi apa aja yg ada di jwt)

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import  List

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
# # cara manual (kita bikin pydantic model khusus untuk handle User Login)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
# # Cara otomatis, pake dependency OAuth2PasswordRequestForm yg ada di library fastapi, dimana ini 
# # udah menginclude model yang memiliki attribute username dan password (bukan email dan password)
# # jadi kalo mau bandingin email yg ada di db, kita bandingin sama field username dari model ini
# # Perlu diperhatikan juga kalo kita make model ini, kita tidak lagi mengirimkan data di opsi Body > RAW JSON (dari postman)
# # Tapi kita akan mengirimkan data dari Body > form-data
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:    # best practice: jangan tampilkan pesan "hey this is the wrong email/password" karena akan memudahkan hacker untuk menebak2 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    password_is_correct = utils.verify(user_credentials.password, user.password)

    if not password_is_correct:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token (JWT) [data berupa payload apa aja yg bakal dimasukkan ke jwt]
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}   # token type: bearer itu untuk nantinya dihandle di fe







