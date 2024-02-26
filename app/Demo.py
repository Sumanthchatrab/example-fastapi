from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class schema(BaseModel):
    title : str
    content : str

mydata = [{"Title":"PythonAPI", "content":"FastApi implementation in Python", "id":1},
          {"Title":"JavaAPI", "content":"FastApi implementation in Java", "id":2}]

def getid(lol):
    for p in mydata:
        if p["id"]==lol:
            return p
        
def find_indexof_post(id):  
    for i,p in enumerate(mydata):
        if p["id"]==id:
            return i

app = FastAPI()
@app.get("/")
async def root():
    return {"Data": mydata}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def root1(newdata: schema):
    mypost = newdata.dict()
    mypost['id'] = randrange(0,9999999)
    mydata.append(mypost)
    return {"New Record": f"{mypost}"}

@app.get("/posts/{id}")
async def getbyid(id: int):
    ourpost = getid(id)
    if not ourpost:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} not found")
    return {"Data": ourpost}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int):
    index = find_indexof_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    mydata.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_posts(id: int, post: schema):
    index = find_indexof_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    updateddata = dict(post)
    updateddata['id'] = id
    mydata[index] = updateddata
    return {"message": updateddata}



