from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, joinedload
from datetime import datetime
from database import Base, obtener_sesion


class MiembroGrupo(Base):
    __tablename__ = "miembros_grupos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    alumno = relationship("Alumno", back_populates="grupos")
    grupo = relationship("Grupo", back_populates="miembros")
    UniqueConstraint("alumno_id", "grupo_id")

    @staticmethod
    def agregar_miembro_grupo(alumno_id: int, grupo_id: int):
        # Import inside method to avoid circular import
        from models.miembro_grupo import MiembroGrupo
        from models.miembro_asociacion import MiembroAsociacion
        from models.grupo import Grupo
        session = obtener_sesion()
        try:
            # First check if student is in the parent association
            grupo = session.query(Grupo).get(grupo_id)
            if not MiembroAsociacion.existe_membresia(alumno_id, grupo.asociacion_id):
                MiembroAsociacion.agregar_miembro(alumno_id, grupo.asociacion_id)

            if not session.query(MiembroGrupo).filter_by(
                alumno_id=alumno_id, 
                grupo_id=grupo_id
            ).first():
                nuevo_miembro = MiembroGrupo(
                    alumno_id=alumno_id,
                    grupo_id=grupo_id
                )
                session.add(nuevo_miembro)
                session.commit()
        finally:
            session.close()

    @staticmethod
    def obtener_miembros_grupo(grupo_id: int):
        session = obtener_sesion()
        try:
            return session.query(MiembroGrupo).options(
                joinedload(MiembroGrupo.alumno)
            ).filter_by(grupo_id=grupo_id).all()
        finally:
            session.close()

    @staticmethod
    def eliminar_miembro_grupo(miembro_id: int):
        session = obtener_sesion()
        try:
            miembro = session.query(MiembroGrupo).get(miembro_id)
            if miembro:
                session.delete(miembro)
                session.commit()
        finally:
            session.close()