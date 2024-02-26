from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schema
from .config import settings
from .database import engine
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)










while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres",
        password="demopassword", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection successfull")
        break

    except Exception as error:
        print("Connection failed with error:", error)
        time.sleep(3)

@app.get("/posts")
async def getbyid():
   cursor.execute(""" SELECT * FROM posts """)
   posts = cursor.fetchall()
   return {"data": posts}

@app.get("/posts/{id}")
async def getbyid(id : int):
   cursor.execute(f""" SELECT * FROM posts where id = %s """, (str(id),))
   posts = cursor.fetchall()
   if not posts:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with {id} does not exist")
   return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED,)
async def createposts(newdata: schema.base):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                    (newdata.title, newdata.content,newdata.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {"Newdata": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int):
    cursor.execute(""" DELETE FROM posts where id=%s RETURNING *""",(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_posts(id: int, newdata: schema.base):
    cursor.execute(""" UPDATE posts SET title = %s, content=%s, published=%s where id=%s RETURNING * """,
                    (newdata.title, newdata.content, newdata.published, str(id)))
    updateddata= cursor.fetchone()
    conn.commit() 
    if updateddata == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return {"message": updateddata}





