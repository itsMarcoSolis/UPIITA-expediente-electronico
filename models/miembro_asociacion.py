from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class MiembroAsociacion(Base):
    __tablename__ = "miembros_asociaciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    asociacion_id = Column(Integer, ForeignKey("asociaciones.id"), nullable=False)
    alumno = relationship("Alumno", back_populates="asociaciones")
    asociacion = relationship("Asociacion", back_populates="miembros")
    UniqueConstraint("alumno_id", "asociacion_id")