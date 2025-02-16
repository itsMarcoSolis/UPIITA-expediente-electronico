from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, obtener_sesion

class Grupo(Base):
    __tablename__ = "grupos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asociacion_id = Column(Integer, ForeignKey("asociaciones.id"), nullable=False)
    nombre_grupo = Column(String, nullable=False)
    asociacion = relationship("Asociacion", back_populates="grupos")
    miembros = relationship("MiembroGrupo", back_populates="grupo")

    @staticmethod
    def agregar_grupo(asociacion_id: int, nombre_grupo: str):
        session = obtener_sesion()
        nuevo_grupo = Grupo(asociacion_id=asociacion_id, nombre_grupo=nombre_grupo)
        session.add(nuevo_grupo)
        session.commit()
        session.close()

    @staticmethod
    def obtener_grupos_por_asociacion(asociacion_id: int):
        session = obtener_sesion()
        grupos = session.query(Grupo).filter_by(asociacion_id=asociacion_id).all()
        session.close()
        return grupos

    @staticmethod
    def actualizar_grupo(grupo_id: int, nuevo_nombre: str):
        session = obtener_sesion()
        grupo = session.query(Grupo).get(grupo_id)
        if grupo:
            grupo.nombre_grupo = nuevo_nombre
            session.commit()
        session.close()

    @staticmethod
    def eliminar_grupo(grupo_id: int):
        session = obtener_sesion()
        grupo = session.query(Grupo).get(grupo_id)
        if grupo:
            session.delete(grupo)
            session.commit()
        session.close()