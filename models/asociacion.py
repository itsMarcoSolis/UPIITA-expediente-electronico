from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Asociacion(Base):
    __tablename__ = "asociaciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    asesor = Column(String, nullable=False)
    miembros = relationship("MiembroAsociacion", back_populates="asociacion")
    grupos = relationship("Grupo", back_populates="asociacion")