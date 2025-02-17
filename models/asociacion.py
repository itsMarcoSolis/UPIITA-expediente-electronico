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