from fastapi import FastAPI
from typing import Union

escuela_musica = FastAPI()

# uvicorn main:escuela_musica --reload

@escuela_musica.get("/")
async def root():
  return {"Hola " : "FastAPI!"}

@escuela_musica.get("/url")
async def url():
  return {"url_escuela" : "https://escuela_armonia.com"}

@escuela_musica.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
  
