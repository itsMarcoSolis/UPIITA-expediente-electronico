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
    carrera = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    asociaciones = relationship("MiembroAsociacion", back_populates="alumno")
    grupos = relationship("MiembroGrupo", back_populates="alumno")
    archivos = relationship("Archivo", back_populates="alumno", cascade="all, delete-orphan")  

    @staticmethod
    def agregar_alumno(boleta, nombre, correo, carrera):
        session = obtener_sesion()
        nuevo_alumno = Alumno(nombre=nombre, boleta=boleta, correo=correo, carrera=carrera)
        session.add(nuevo_alumno)
        session.commit()
        session.close()

    @staticmethod
    def obtener_alumnos():
        session = obtener_sesion()
        alumnos = session.query(Alumno).all()
        session.close()
        return alumnos

    @staticmethod
    def editar_alumno(alumno_id, new_boleta, new_nombre, new_correo, new_carrera):
        session = obtener_sesion()
        alumno = session.query(Alumno).filter_by(id=alumno_id).first()
        if alumno:
            alumno.boleta = new_boleta
            alumno.nombre = new_nombre
            alumno.correo = new_correo
            alumno.carrera = new_carrera
            session.commit()
        session.close()
