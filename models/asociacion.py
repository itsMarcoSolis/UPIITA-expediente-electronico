from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base, obtener_sesion

class Asociacion(Base):
    __tablename__ = "asociaciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    asesor = Column(String, nullable=False)
    miembros = relationship("MiembroAsociacion", back_populates="asociacion")
    grupos = relationship("Grupo", back_populates="asociacion")
    archivos = relationship("Archivo", back_populates="asociacion", cascade="all, delete-orphan")

    @staticmethod
    def agregar_asociacion(nombre: str, asesor: str):
        session = obtener_sesion()
        nueva_asociacion = Asociacion(nombre=nombre, asesor=asesor)
        session.add(nueva_asociacion)
        session.commit()
        session.close()

    @staticmethod
    def obtener_asociaciones():
        session = obtener_sesion()
        asociaciones = session.query(Asociacion).all()
        session.close()
        return asociaciones

    @staticmethod
    def editar_asociacion(asociacion_id: int, nuevo_nombre: str, nuevo_asesor: str):
        """
        Updates the name and advisor of an existing association.
        :param asociacion_id: ID of the association to update.
        :param nuevo_nombre: New name of the association.
        :param nuevo_asesor: New advisor of the association.
        """
        session = obtener_sesion()
        asociacion = session.query(Asociacion).filter_by(id=asociacion_id).first()

        if asociacion:
            asociacion.nombre = nuevo_nombre
            asociacion.asesor = nuevo_asesor
            session.commit()

        session.close()
