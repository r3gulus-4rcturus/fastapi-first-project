from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# format connection string untuk database postgresql
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip address>/<hostname>/<database_name>'

# btw ini bad practice, karena kita gaboleh ngehardcode username dan password dr db kita 
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine untuk establish a connection sqlalchemy dengan postgresql
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# establish session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
# jadi tiap kita ada request, kita bakal bikin session baru
# dengan database, lalu kita kirim sql query ke database, terima
# hasilnya, lalu close sessionnya
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ini cara mengconnect ke database kalo ga pake sqlalchemy
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor  # agar saat melakukan sql operation, nama column ditampilkan
# while True:
#     try:
#         # in reality, ini adalah bad practice. Ini adalah development database, karena kalo production
#         # gamungkin dihost sama localhost. Ini juga langsung menghardcode user dan password, yg kalo dicommit bakal
#         # langsung ketauan user dan passwordnya sama dunia luar
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='bismillahmenanghackathon', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull!')
#         break
#     except Exception as error:
#         print("Connecting to database fail")
#         print("Error: {error}")
#         time.sleep(2)