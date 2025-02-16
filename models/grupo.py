from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Grupo(Base):
    __tablename__ = "grupos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asociacion_id = Column(Integer, ForeignKey("asociaciones.id"), nullable=False)
    nombre_grupo = Column(String, nullable=False)
    asociacion = relationship("Asociacion", back_populates="grupos")
    miembros = relationship("MiembroGrupo", back_populates="grupo")