from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

escuela_musica = FastAPI()

# Inicia el server -> uvicorn alumnos:escuela_musica --reload

# Entidad alumno
class Alumno(BaseModel):
    id: int
    nombre: str
    apellidos: str
    edad: int
    teléfono: str
    correo: str
    familiar_id: int

alumnos_fake_db = [Alumno(id=1, nombre="Juan", apellidos="Pérez", edad=25, teléfono="123456789", correo="juan@example.com", familiar_id=2),
                   Alumno(id=2, nombre="María", apellidos="González", edad=30, teléfono="987654321", correo="maria@example.com", familiar_id=1),
                   Alumno(id=3, nombre="Pedro", apellidos="Martínez", edad=20, teléfono="456789123", correo="pedro@example.com", familiar_id=3)]


@escuela_musica.get("/alumnosjson", response_model=List[Alumno])
async def alumnosjson():
  return [{"id": 1, "nombre": "Juan", "apellidos": "Pérez", "edad": 25, "teléfono": "123456789", "correo": "juan@example.com", "familiar_id": 2},
          {"id": 2, "nombre": "María", "apellidos": "González", "edad": 30, "teléfono": "987654321", "correo": "maria@example.com", "familiar_id": 1},
          {"id": 3, "nombre": "Pedro", "apellidos": "Martínez", "edad": 20, "teléfono": "456789123", "correo": "pedro@example.com", "familiar_id": 3}]


@escuela_musica.get("/alumnos", response_model=List[Alumno])
async def alumnos():
  return alumnos_fake_db

@escuela_musica.get("/alumno/{id}", response_model=Alumno) # Path parameter
async def alumno(id : int):
  return buscar_alumno(id)

@escuela_musica.get("/alumno/", response_model=Alumno) # Query parameter
async def alumno(id : int):
  return buscar_alumno(id)
  
    
@escuela_musica.post("/alumno/", response_model=Alumno, status_code=201)
async def alumno_post(alumno: Alumno):
  
  if type(buscar_alumno(alumno.id)) == Alumno:
    raise HTTPException(status_code=204, detail="el alumno ya existe")
  
  else: 
    alumnos_fake_db.append(alumno)
    return alumno

@escuela_musica.put("/alumno/", response_model=Alumno, status_code=201)
async def alumno_put(alumno: Alumno):
    
    encontrado = False
    
    for index, alumno_archivado in enumerate(alumnos_fake_db):
        if alumno_archivado.id == alumno.id:
            alumnos_fake_db[index] = alumno
            encontrado = True
            
    if not encontrado:
      raise HTTPException(status_code=404, detail="alumno no encontrado")
      
    else:
      return alumno


@escuela_musica.delete("/alumno/{id}")
async def alumno_delete(id: int):
  
  encontrado = False
  
  for index, alumno_archivado in enumerate(alumnos_fake_db):
        if alumno_archivado.id == id:
            del alumnos_fake_db[index]
            encontrado = True
            return { "alumno eliminado correctamente" }
            
  if not encontrado:
      raise HTTPException(status_code=404, detail="alumno no encontrado")
    
			
  



def buscar_alumno(id: int):
  alumnos = filter(lambda alumno: alumno.id == id, alumnos_fake_db) # Filtra los alumnos con el id dado
  try:
    return list(alumnos)[0]
  except:
    return  { "error" : "alumno no encontrado" }