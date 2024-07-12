from sqlalchemy import Table, Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

profesores = Table(
    "profesores", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("nombre", String(50), nullable=False)
)

alumnos = Table(
    "alumnos", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("nombre", String(50), nullable=False),
    Column("apellidos", String(50), nullable=False),
    Column("edad", Integer, nullable=False),
    Column("familiar_id", Integer, ForeignKey("alumnos.id"))
)

datos_sensibles = Table(
    "datos_sensibles", metadata,
    Column("alumno_id", Integer, primary_key=True),
    Column("email", String(100)),
    Column("telefono", String(20)),
    ForeignKeyConstraint(["alumno_id"], ["alumnos.id"])
)

clases = Table(
    "clases", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("nombre", String(50), nullable=False),
    Column("profesor_id", Integer, ForeignKey("profesores.id"), nullable=False),
    Column("precio_base", DECIMAL(5, 2), nullable=False),
    Column("tipo_pack", String(20), nullable=False)
)

niveles = Table(
    "niveles", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("clase_id", Integer, ForeignKey("clases.id"), nullable=False),
    Column("nivel", String(20), nullable=False)
)

clase_profesor = Table(
    "clase_profesor", metadata,
    Column("clase_id", Integer, ForeignKey("clases.id", ondelete="CASCADE")),
    Column("profesor_id", Integer, ForeignKey("profesores.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("clase_id", "profesor_id")
)

alumnos_clases = Table(
    "alumnos_clases", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("alumno_id", Integer, ForeignKey("alumnos.id"), nullable=False),
    Column("clase_id", Integer, ForeignKey("clases.id"), nullable=False),
    Column("nivel_id", Integer, ForeignKey("niveles.id"), nullable=False)
)

precios = Table(
    "precios", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("tipo_pack", String(20), nullable=False),
    Column("precio_base", DECIMAL(5, 2), nullable=False),
    Column("descuento_segunda", DECIMAL(5, 2), nullable=False),
    Column("descuento_tercera", DECIMAL(5, 2), nullable=False)
)