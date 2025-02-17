import os
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, joinedload
from datetime import datetime
from database import Base, obtener_sesion
from models.archivo import Archivo

class Grafico(Base):
    __tablename__ = "graficos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Type of the grafico
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relationship to Archivo (one Grafico -> one Archivo)
    archivo = relationship("Archivo", back_populates="grafico", cascade="all, delete-orphan", uselist=False)

    @staticmethod
    def agregar_grafico(nombre, tipo):
        """
        Add a new Grafico entry.
        :param nombre: Name of the grafico
        :param tipo: Type of the grafico
        """
        session = obtener_sesion()
        nuevo_grafico = Grafico(nombre=nombre, tipo=tipo)
        session.add(nuevo_grafico)
        session.commit()
        session.refresh(nuevo_grafico)  # Get the new ID for file association
        session.close()
        return nuevo_grafico.id  # Return ID to link with the file

    @staticmethod
    def eliminar_grafico(grafico_id):
        """
        Delete a Grafico entry and its associated file.
        :param grafico_id: ID of the grafico to delete
        """
        session = obtener_sesion()
        grafico = session.query(Grafico).filter_by(id=grafico_id).first()


        # Fetch the linked archivo before deleting the grafico
        archivo = session.query(Archivo).filter_by(grafico_id=grafico_id).first()

        # If a linked file exists, delete it from disk
        if os.path.exists(archivo.ruta_archivo):
            os.remove(archivo.ruta_archivo)
        
        # Delete the Archivo entry from the database
        session.delete(archivo)

        # Delete the Grafico entry
        session.delete(grafico)
        session.commit()

        session.close()

    @staticmethod
    def obtener_graficos():
        session = obtener_sesion()
        try:
            return session.query(Grafico).options(
                joinedload(Grafico.archivo)  # Eager load the archivo relationship
            ).all()
        finally:
            session.close()
