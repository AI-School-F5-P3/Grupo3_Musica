from fastapi import FastAPI
from pydantic import BaseModel

escuela_musica = FastAPI()

# Inicia el server: uvicorn alumnos:escuela_musica --reload

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


@escuela_musica.get("/alumnosjson")
async def alumnosjson():
  return [{"id": 1, "nombre": "Juan", "apellidos": "Pérez", "edad": 25, "teléfono": "123456789", "correo": "juan@example.com", "familiar_id": 2},
          {"id": 2, "nombre": "María", "apellidos": "González", "edad": 30, "teléfono": "987654321", "correo": "maria@example.com", "familiar_id": 1},
          {"id": 3, "nombre": "Pedro", "apellidos": "Martínez", "edad": 20, "teléfono": "456789123", "correo": "pedro@example.com", "familiar_id": 3}]


@escuela_musica.get("/alumnos")
async def alumnos():
  return alumnos_fake_db

@escuela_musica.get("/alumno/{id}") # Path parameter
async def alumno(id : int):
  return buscar_alumno(id)

@escuela_musica.get("/alumno/") # Query parameter
async def alumno(id : int):
  return buscar_alumno(id)
  
    
@escuela_musica.post("/alumno/")
async def alumno_post(alumno: Alumno):
  if type(buscar_alumno(alumno.id)) == Alumno:
   return { "error" : "El alumno ya existe" }
  else: 
    alumnos_fake_db.append(alumno)
  return alumno

@escuela_musica.put("/alumno/")
async def alumno_put(alumno: Alumno):
    
    encontrado = False
    
    for index, alumno_archivado in enumerate(alumnos_fake_db):
        if alumno_archivado.id == alumno.id:
            alumnos_fake_db[index] = alumno
            encontrado = True
            
    if not encontrado:
        return { "error" : "Alumno no encontrado" }
			
  



def buscar_alumno(id: int):
  alumnos = filter(lambda alumno: alumno.id == id, alumnos_fake_db) # Filtra los alumnos con el id dado
  try:
    return list(alumnos)[0]
  except:
    return  { "error" : "Alumno no encontrado" }