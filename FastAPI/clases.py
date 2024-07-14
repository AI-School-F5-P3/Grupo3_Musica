from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

escuela_musica = FastAPI()

# Entidad clase
class Clase(BaseModel):
  id:int
  nombre: str
  profesor_id: int
  precio_base: float
  tipo_pack: str

clases_fake_db = [Clase(id=1, nombre="Guitarra", profesor_id=1, precio_base=30.0, tipo_pack="individual"),
                  Clase(id=2, nombre="Piano", profesor_id=2, precio_base=35.0, tipo_pack="individual"),
                  Clase(id=3, nombre="Batería", profesor_id=3, precio_base=40.0, tipo_pack="individual")]

@escuela_musica.get("/clases", response_model=List[Clase])
async def clases():
  return clases_fake_db