# untuk menyimpan pydantic model Settings()
# yang berfungsi untuk mengambil environment variable dari user variables
# dan melakukan validasi (type validation dan juga validasi apakah variabel tersebut ada)

# SEMUA ENVIRONMENT VARIABLE DISIMPEN DI .env (ini hanya untuk DEVELOPMENT, bukan PRODUCTION)
# kalo di production kita harus setting environment variables di mesinnya langsung
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    # gapapa pake huruf kecil, karena nanti pydantic akan otomatis ngehandle bds. case insensitive
    # jadi, pydantic akan otomatis MENCARI variabel database_password dari variabel2 di .env
    # kalo ada, langsung dimasukin ke variabel database_password, kalo ga ada akan ngeluarin error (missing)
    # pydantic juga akan melakukan validasi tipe data, misalkan variabelnya int maka dia akan ngefetch 
    # environment variable yg berupa string lalu ngetypecast ke int, dia bakal error kalo gabisa di casting
    # path: int #contohnya kaya gini, ya jelas error karena variabel PATH yg ada di env variabel itu berupa string  
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env" # semua variable diambil dari sini .env

settings = Settings()