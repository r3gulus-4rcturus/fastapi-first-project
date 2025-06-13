from fastapi import FastAPI
from . import models # untuk mengakses semua model yg udah kita buat (models.Post, ...)
from .database import engine

# semakin lama, program kita akan semakin complex, semakin banyak path operation yg dibuat
# Oleh karena itu, fastAPI memiliki cara untuk melakukan "split" atau mengelompokkan
# Path-path operation berdasarkan contextnya (path operation yg handle table User dikelompokin, handle table Post dikelompokin etc.) 
# caranya: Bikin folder "routers" lalu buat file .py di dalamnya yg masing-masing file handle specific routes yang handle path operation specific terhadap suatu table 
# lalu jangan lupa importkan
from .routers import post, user, auth, vote

from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# GENERATE DATABASE TABLES using SQLALCHEMY ORM
# ini berfungsi untuk menkonfigurasi models/tables pada database
# pertama, yg akan dilakukannya adalah memeriksa untuk tiap model di models.py
# apakah ada nama table di database yang sama dengan nama model saat ini
# kalo SUDAH, yaudah biarin, kalo BELUM, dibikinin
# Jadi, kalo kita modif attribute di dalam model, itu ga akan otomatis keubah juga di table di database, karena
# dia ini ngiranya table yg bersesuaian dg model tersebut suda dibikin, jdi ga disentuh2 lagi
# models.Base.metadata.create_all(bind=engine)

# kalo kita pake database migration tools alembic, 
# maka gaperlu lagi pake models.Base.metadata.create_all(bind=engine) kaya di atas

app = FastAPI()     # Instance API

# list domain yg boleh minta request ke API ini
origins = ["*"] # artinya semua domain boleh request ke API ini

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # artinya semua method (GET, POST, PUT, DELETE, PATCH) boleh request ke API ini
    allow_headers=["*"], # artinya semua header boleh request ke API ini
)

# sambungkan router yang telah dibuat dengan instance API yg ada di main
app.include_router(user.router) # "kalo terjadi request path operation, periksa terlebih dahulu method2 path operation yg ada di dalam route ini
app.include_router(post.router) # apakah ada method yg cocok. Kalo ga ada, baru uperiksa method2 path operation di file main (file)"
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API!"}

# @app.get("/sqlalchemy")
# def get_sqlalchemy(db: Session = Depends(get_db)):
#     # ini merupakan cara query menggunakan sqlalchemy (ORM)
#     # kalo kita coba print db.query(models.Post) , isinya adalah RAW SQL QUERY 
#     # yg digunakan jika kita mau query pake sql biasa
#     # Nah, untuk ngeRUN query itu, kita perlu pipeline pake method lagi (bisa .all(), .filter(), ...)
#     posts = db.query(models.Post).all()
#     return {"status": posts} 

# POSTMAN ENVIRONMENT
# nyimpen variabel/nilai yg dipake berulang2
# Contoh: URL domain, JWT, dsb.
# aksesnya bisa pake {{URL}}. Jangan lupa di request kita set environment sesuai yg udah kita bikin
# kalo mau set environment variable otomatis, pergi ke scripts > post res, (misalkan mau set jwt otomatis setelah kita hit endpoint login)
# pm.environment.set("JWT", pm.response.json().access_token)
# Jadi, klo kita send request login dan berhasil, kan kita pasti dapat response berupa json yg ada field access_tokennya
# nah itu otomatis akan tersimpan di environment kita sebagai value, keynya JWT  

