'''
Es necesario instalar:
FastAPI.
sqlalchemy databases <- para la conexión a la base de datos. 
asyncpg pydantic <- para la conexión a la base de datos. 

'''

from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/escuela_musica"
# <user>: El nombre de usuario de la base de datos PostgreSQL.
# <password>: La contraseña del usuario de la base de datos PostgreSQL.
# <localhost>: La dirección del servidor donde está alojada tu base de datos. Si está en tu máquina local, utiliza localhost.

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)