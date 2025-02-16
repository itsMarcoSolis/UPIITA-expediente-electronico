from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base, obtener_sesion

class Alumno(Base):
    __tablename__ = "alumnos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    boleta = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    asociaciones = relationship("MiembroAsociacion", back_populates="alumno")
    grupos = relationship("MiembroGrupo", back_populates="alumno")

    @staticmethod
    def agregar_alumno(boleta, nombre, correo):
        session = obtener_sesion()
        nuevo_alumno = Alumno(nombre=nombre, boleta=boleta, correo=correo)
        session.add(nuevo_alumno)
        session.commit()
        session.close()

    @staticmethod
    def obtener_alumnos():
        session = obtener_sesion()
        alumnos = session.query(Alumno).all()
        session.close()
        return alumnos