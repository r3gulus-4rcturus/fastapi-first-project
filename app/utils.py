# Store bunch of utilites function

# untuk store password di database, bad practice apabila kita store passwordnya berupa plain string
# Rentan banget dicuri datanya sama hacker, kalo db kita ke leak. jadi solusinya: pake hashing
# import library for hashing the password
from passlib.context import CryptContext # untuk handle hashing password (terdapat banyak pilihan opsi algoritma hashing di library ini, salah satunya bcrypt)
# choose hashing algorithm that we want to use (for example: bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# untuk hashing password baru
def hash(password: str):
    return pwd_context.hash(password)

# untuk melakukan verify password yg dikirim oleh user (apakah udh bener/ngga)
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)





