from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from databases import Database

app = FastAPI()

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/escuela_musica"

database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = database
    try:
        yield db
    finally:
        db.close()

@app.post("/profesores/", response_model=Profesor)
async def create_profesor(profesor: ProfesorCreate, db: Session = Depends(get_db)):
    query = profesores.insert().values(nombre=profesor.nombre)
    last_record_id = await db.execute(query)
    return {**profesor.dict(), "id": last_record_id}

@app.get("/profesores/{profesor_id}", response_model=Profesor)
async def read_profesor(profesor_id: int, db: Session = Depends(get_db)):
    query = profesores.select().where(profesores.c.id == profesor_id)
    profesor = await db.fetch_one(query)
    if profesor is None:
        raise HTTPException(status_code=404, detail="Profesor not found")
    return profesor

@app.put("/profesores/{profesor_id}", response_model=Profesor)
async def update_profesor(profesor_id: int, profesor: ProfesorCreate, db: Session = Depends(get_db)):
    query = profesores.update().where(profesores.c.id == profesor_id).values(nombre=profesor.nombre)
    await db.execute(query)
    return {**profesor.dict(), "id": profesor_id}

@app.delete("/profesores/{profesor_id}")
async def delete_profesor(profesor_id: int, db: Session = Depends(get_db)):
    query = profesores.delete().where(profesores.c.id == profesor_id)
    await db.execute(query)
    return {"message": "Profesor deleted successfully"}

# CRUD para alumnos, clases, niveles, etc.
