from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2   # untuk specify file di directory sebelumnya, tambahkan ..                     # untuk mengakses semua model yg udah kita buat (models.Post, ...)
from ..database import get_db
from typing import  List, Optional
from sqlalchemy import func # untuk akses function seperti COUNT()

router = APIRouter(
    prefix="/posts", # di setiap path operation, route/url akan memiliki prefix /posts
                    # misalkan @router.get(/{id}) berarti untuk hit endpoint api ini urlnya: /posts/{id}
    tags=['Posts']  # untuk mengelompokkan path operation yg ada di dalam file ini ke dalam satu kelompok di documentation
)

@router.get("/", response_model=List[schemas.PostResponseWithVotes])
def get_posts(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10,# limit default = 10 (limit disini adalah query parameter)
                    skip: int = 0,# cara pass query param: posts?limit=8&skip=5&search=aku%20jakarta
                    search: Optional[str] = ""):   #                      %20 = spasi "aku jakarta"
                                       
    # SQL OPERATOIN USING RAW SQL
    # # enter sql operation using .execute()
    # cursor.execute("""SELECT * FROM posts""")
    # # retrieve all data using fetchall (if u want to retrieve 1 data, use fetchone, like if u want to search by id)
    # # then, store it in a variable
    # posts = cursor.fetchall()

    # SQL OPERATION USING SQLALCHEMY ORM 
    # posts = db.query(models.Post)
    # limit untuk limit, offset untuk skip, filter .contains untuk search
    # kalo data cuma 60, kita skip 100, maka API ga akan nampilin data apa2

    # Join dengan sql query ini
    # SELECT posts.*, COUNT(user_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;
    # masalahnya, default kalo kita pake .join() di sqlalchemy itu LEFT INNER JOIN, sedangkan di sql query defaultnya OUTER, 
    # karena kita emang mau pake OUTER, jadi kita perlu specify di dalam method .join(isouter = True) 
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(
                skip).all()

    return posts   # fastAPI akan otomatis mengconvert menjadi json

# get individual post by ID (post, singular, not posts)
@router.get("/{id}", response_model=schemas.PostResponseWithVotes) 
def get_post(id: int, db: Session = Depends(get_db)):  # langsung declare kalo id harus berupa int, jadi fastapi akan melakukan validasi otomatis (kita gaperlu try except)
    # SQL OPERATION USING RAW SQL
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    # SQL OPERATION USING SQLALCHEMY
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
            models.Post.id).filter(models.Post.id == id).first()   # lebih efisien dari .all() karena kita tau post dengan id tersebut hanya ada satu
                                                                        # kalo .all(), klo udah ketemu dengan 1 post, dia bakal tetep nyari lagi semua post 
                                                                        # dengan id tersebut, tidak efisien.

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail      = f'Post with id: {id} was not found')
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)    # anytime we create an entity, the status code must be 201
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: schemas.TokenData = Depends(oauth2.get_current_user)): # method ini memerlukan dependency oauth2, dimana user harus login terlebih dahulu baru bisa invoke method ini)
                 # jadi dengan adanya dependency, endpoint ini hanya akan dijalankan apabila kita menyertakan TOKEN dengan cara
                 # di postman > headers > tambain "Authorization" lalu isi field "Bearer <JWT>" atau
                 # postman > auth > pilih bearer token > isi filed <JWT> nya
    
    # SQL OPERATION USING RAW SQL
    # # kenapa gak gini aja? karena ini RENTAN TERHADAP SQL INJECTION (JANGAN BIASAIN MAKE formatting {} )
    # # cursor.execute(f'INSERT INTO posts (title, content, published) VALUES ({new_post.title}, {new_post.content}, {new_post.published})')
    # # kalo kaya dibawah ini (c style formatting) keamanan akan lebih terjamin
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (new_post.title, new_post.content, new_post.published))
    # post = cursor.fetchone()

    # # commit the changes to connection (not to cursor)
    # conn.commit()

    # SQL OPERATION USING SQLALCHEMY ORM 
    # bikin instance baru berdasarkan Modelnya 
    # new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)    # cara susah
    # new_post = models.Post(**new_post.dict())       # cara mudah, dengan meng-unpack new_post.dict() yg berupa dictionary pydantic model.
                                                    # **new_post.dict() isinya => title=new_post.title, content=new_post.content, published=new_post.published
    new_post = models.Post(owner_id=current_user.id, **new_post.dict()) 
    db.add(new_post)        # add to database
    db.commit()             # commit changes to database
    db.refresh(new_post)    # retrieve the instance that have been created, store back to new_post variable 

    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)    # anytime we create an entity, the status code must be 201
def delete_posts(id: int, db: Session = Depends(get_db),
                 current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # # SQL OPERATION USING RAW SQL    
    # # deleting a post
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # # jangan lupa commit karena ini memodifikasi database
    # conn.commit()

    # SQL OPERATION USING SQLALCHEMY    
    post_query = db.query(models.Post).filter(models.Post.id == id)   # ini masih berupa query, bukan post
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail      = f'Post with id: {id} was not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)  # lakukan query delete; ini adlaah most reliable operation: synchronize_session=False
    db.commit()

    return Response(status_code =status.HTTP_204_NO_CONTENT)    # this is the best practices

@router.put("/{id}", response_model=schemas.PostResponse)
def update_posts(new_post: schemas.PostCreate, id: int, db: Session = Depends(get_db),
                 current_user = Depends(oauth2.get_current_user)):
    # # SQL OPERATION USING RAW SQL    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (new_post.title, new_post.content, new_post.published, str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    print(current_user.email)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail      = f'Post with id: {id} was not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    
    # post_query.update({'title': new_post.title, 'content': new_post.content, 'published': new_post.published}, synchronize_session=False)  lebih simpel yg bawah:
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
