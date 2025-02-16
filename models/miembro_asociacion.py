from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base, obtener_sesion
import sqlalchemy.orm

class MiembroAsociacion(Base):
    __tablename__ = "miembros_asociaciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    asociacion_id = Column(Integer, ForeignKey("asociaciones.id"), nullable=False)
    alumno = relationship("Alumno", back_populates="asociaciones")
    asociacion = relationship("Asociacion", back_populates="miembros")
    UniqueConstraint("alumno_id", "asociacion_id")

    @staticmethod
    def agregar_miembro(alumno_id: int, asociacion_id: int):
        session = obtener_sesion()
        if not MiembroAsociacion.existe_membresia(alumno_id, asociacion_id):
            nuevo_miembro = MiembroAsociacion(
                alumno_id=alumno_id,
                asociacion_id=asociacion_id
            )
            session.add(nuevo_miembro)
            session.commit()
        session.close()

    @staticmethod
    def eliminar_miembro(miembro_id: int):
        session = obtener_sesion()
        miembro = session.query(MiembroAsociacion).get(miembro_id)
        if miembro:
            session.delete(miembro)
            session.commit()
        session.close()

    @staticmethod
    def obtener_miembros_por_asociacion(asociacion_id: int):
        session = obtener_sesion()
        miembros = session.query(MiembroAsociacion).options(
            sqlalchemy.orm.joinedload(MiembroAsociacion.alumno)
        ).filter_by(asociacion_id=asociacion_id).all()
        session.close()
        return miembros

    @staticmethod
    def existe_membresia(alumno_id: int, asociacion_id: int) -> bool:
        session = obtener_sesion()
        exists = session.query(MiembroAsociacion).filter_by(
            alumno_id=alumno_id,
            asociacion_id=asociacion_id
        ).first() is not None
        session.close()
        return exists