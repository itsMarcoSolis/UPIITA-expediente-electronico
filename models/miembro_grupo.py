from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class MiembroGrupo(Base):
    __tablename__ = "miembros_grupos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    alumno = relationship("Alumno", back_populates="grupos")
    grupo = relationship("Grupo", back_populates="miembros")
    UniqueConstraint("alumno_id", "grupo_id")
