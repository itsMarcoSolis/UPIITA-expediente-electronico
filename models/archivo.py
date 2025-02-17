from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from database import Base, obtener_sesion, app_data_path

# Define paths for storing files
FILES_DIR = os.path.join(app_data_path, "files")
ALUMNOS_FILES_DIR = os.path.join(FILES_DIR, "alumnos")
ASOCIACIONES_FILES_DIR = os.path.join(FILES_DIR, "asociaciones")
GRAFICOS_FILES_DIR = os.path.join(FILES_DIR, "graficos")

# Ensure directories exist
os.makedirs(FILES_DIR, exist_ok=True)

class Archivo(Base):
    __tablename__ = "archivos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_archivo = Column(String, nullable=False)
    ruta_archivo = Column(String, nullable=False, unique=True)
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    # The file can be linked to an Alumno, Asociacion, or Grafico
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=True)
    asociacion_id = Column(Integer, ForeignKey("asociaciones.id"), nullable=True)
    grafico_id = Column(Integer, ForeignKey("graficos.id"), nullable=True)

    alumno = relationship("Alumno", back_populates="archivos")
    asociacion = relationship("Asociacion", back_populates="archivos")
    grafico = relationship("Grafico", back_populates="archivo")

    @staticmethod
    def agregar_archivo(nombre_archivo, contenido, tipo, entity_id):
        """
        Add a file linked to an Alumno, Asociacion, or Grafico.
        :param nombre_archivo: Name of the file
        :param contenido: File binary content
        :param tipo: 'alumno', 'asociacion', or 'grafico'
        :param entity_id: ID of the associated entity
        """
        session = obtener_sesion()

        # Determine where to store the file
        if tipo == "alumno":
            ruta_directorio = os.path.join(ALUMNOS_FILES_DIR, str(entity_id))
            archivo = Archivo(alumno_id=entity_id)
        elif tipo == "asociacion":
            ruta_directorio = os.path.join(ASOCIACIONES_FILES_DIR, str(entity_id))
            archivo = Archivo(asociacion_id=entity_id)
        elif tipo == "grafico":
            ruta_directorio = GRAFICOS_FILES_DIR
            archivo = Archivo(grafico_id=entity_id)
        else:
            raise ValueError("Tipo de archivo no válido. Usa 'alumno', 'asociacion' o 'grafico'.")

        # Ensure entity-specific directory exists
        os.makedirs(ruta_directorio, exist_ok=True)

        # Store the file
        ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
        with open(ruta_archivo, "wb") as f:
            f.write(contenido)

        # Save file metadata in DB
        archivo.nombre_archivo = nombre_archivo
        archivo.ruta_archivo = ruta_archivo
        session.add(archivo)
        session.commit()
        session.close()

    @staticmethod
    def eliminar_archivo(archivo_id):
        """
        Delete a file from storage and database.
        """
        session = obtener_sesion()
        archivo = session.query(Archivo).filter_by(id=archivo_id).first()

        if archivo:
            # Delete file from disk
            if os.path.exists(archivo.ruta_archivo):
                os.remove(archivo.ruta_archivo)

            # Remove database entry
            session.delete(archivo)
            session.commit()

        session.close()

    @staticmethod
    def obtener_archivos(tipo, entity_id):
        """
        Get all files for a given student, association, or grafico.
        :param tipo: 'alumno', 'asociacion', or 'grafico'
        :param entity_id: The entity ID
        """
        session = obtener_sesion()
        if tipo == "alumno":
            archivos = session.query(Archivo).filter_by(alumno_id=entity_id).all()
        elif tipo == "asociacion":
            archivos = session.query(Archivo).filter_by(asociacion_id=entity_id).all()
        elif tipo == "grafico":
            archivos = session.query(Archivo).filter_by(grafico_id=entity_id).all()
        else:
            raise ValueError("Tipo no válido.")

        session.close()
        return archivos
