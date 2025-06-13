# every MODEL in this python file represent a TABLE in the database

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

# make a schema
class Post(Base):
    # define the table name
    __tablename__ = 'posts'

    # server_default untuk mengisi value suatu constraint ke dalam database 
    # (menggunakan langauge database tersebut, misalnya now(), true, dlm postgresql)
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    #foreign key (parameter pertama dari ForeignKey <namaClass>.<namaField>)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # NOT a foreign key, tapi nyimpen data dari tabel lain: relationship 
    # jadi kita nyuruh sqlalchemy buat ngefetch data tambahan setelah dapet owner_id
    # intinya nyimpen email dari instance user yg memiliki id=owner_id
    owner = relationship("User")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)    # unique = attribute ini harus berbeda2 untuk tiap entry (tdk boleh ada User dengan email yg sama) 
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

 






