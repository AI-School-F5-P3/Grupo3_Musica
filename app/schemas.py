from pydantic import BaseModel
from typing import Optional, List

class ProfesorBase(BaseModel):
    nombre: str

class ProfesorCreate(ProfesorBase):
    pass

class Profesor(ProfesorBase):
    id: int

    class Config:
        orm_mode: True

class AlumnoBase(BaseModel):
    nombre: str
    apellidos: str
    edad: int
    familiar_id: Optional[int] = None

class AlumnoCreate(AlumnoBase):
    email: str
    telefono: str

class Alumno(AlumnoBase):
    id: int

    class Config:
        orm_mode: True

class DatosSensiblesBase(BaseModel):
    email: str
    telefono: str

class DatosSensiblesCreate(DatosSensiblesBase):
    pass

class DatosSensibles(DatosSensiblesBase):
    alumno_id: int

    class Config:
        orm_mode: True

# Definimos esquemas adicionales para clases, niveles, etc.
