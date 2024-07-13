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

alumnos_fake_db = [Alumno(id=1, nombre="Juan", apellidos="Pérez", edad=25, teléfono="123456789", correo="juan@ealumnoample.com", familiar_id=2),
                   Alumno(id=2, nombre="María", apellidos="González", edad=30, teléfono="987654321", correo="maria@ealumnoample.com", familiar_id=1),
                   Alumno(id=3, nombre="Pedro", apellidos="Martínez", edad=20, teléfono="456789123", correo="pedro@ealumnoample.com", familiar_id=3)]


@escuela_musica.get("/alumnosjson")
async def alumnosjson():
  return [{"id": 1, "nombre": "Juan", "apellidos": "Pérez", "edad": 25, "teléfono": "123456789", "correo": "juan@ealumnoample.com", "familiar_id": 2},
          {"id": 2, "nombre": "María", "apellidos": "González", "edad": 30, "teléfono": "987654321", "correo": "maria@ealumnoample.com", "familiar_id": 1},
          {"id": 3, "nombre": "Pedro", "apellidos": "Martínez", "edad": 20, "teléfono": "456789123", "correo": "pedro@ealumnoample.com", "familiar_id": 3}]


@escuela_musica.get("/alumnos")
async def alumnos():
  return alumnos_fake_db

@escuela_musica.get("/alumno/{id}")
async def alumno(id : int):
  alumnos = filter(lambda alumno: alumno.id == id, alumnos_fake_db)
  try:
    return list(alumnos)[0]
  except:
    return "Alumno no encontrado"