import os
from nicegui import ui
from database import obtener_sesion
from models.archivo import Archivo
from models.grafico import Grafico

"""
    dialog parameter passed to the functions here has to be 
    initialized on the page context.
"""

def subir_archivo_ui(dialog, tipo, entity):
    """
    Creates an upload UI for files related to an Alumno, Asociacion, or Grafico.
    :param tipo: 'alumno', 'asociacion', or 'grafico'
    :param entity: Object representing the entity (Alumno, Asociacion, or Grafico)
    """
    ui.upload(
        label="Subir Archivo",
        auto_upload=True,
        on_upload=lambda file: agregar_archivo(dialog, file, tipo, entity)
    )

def agregar_archivo(dialog, file, tipo, entity):
    """
    Saves the uploaded file and associates it with an entity.
    Ensures that duplicate file names do not exist for the same entity.

    :param file: Uploaded file object
    :param tipo: 'alumno', 'asociacion', or 'grafico'
    :param entity: Object representing the entity (Alumno, Asociacion, or Grafico)
    """
    # If the entity is a grafico, we enforce a single file per grafico.
    if tipo == "grafico":
        archivos_existentes = Archivo.obtener_archivos(tipo, entity.id)
        if archivos_existentes:
            ui.notify(f"El gráfico '{entity.nombre}' ya tiene un archivo asociado.", color="red")
            return
    
    # Check for duplicates only in alumnos and asociaciones
    elif tipo in ["alumno", "asociacion"]:
        archivos_existentes = Archivo.obtener_archivos(tipo, entity.id)
        if any(archivo.nombre_archivo == file.name for archivo in archivos_existentes):
            ui.notify(f"El archivo '{file.name}' ya existe en este {tipo}.", color="red")
            return

    # Save the file if it's not a duplicate
    Archivo.agregar_archivo(file.name, file.content.read(), tipo, entity.id)
    
    # Refresh the corresponding UI
    if tipo == "grafico":
        administrar_graficos(dialog)
    else:
        mostrar_archivos(dialog, tipo, entity)

def eliminar_archivo(dialog, archivo_id, tipo, entity):
    """
    Deletes a file from storage and database.
    :param archivo_id: ID of the file to delete
    :param tipo: 'alumno', 'asociacion', or 'grafico'
    :param entity: Object representing the entity
    """
    Archivo.eliminar_archivo(archivo_id)
    
    # Refresh UI accordingly
    if tipo == "grafico":
        administrar_graficos(dialog)
    else:
        mostrar_archivos(dialog, tipo, entity)

def abrir_archivo(ruta):
    """
    Opens a file with the default system program.
    :param ruta: Path to the file
    """
    os.startfile(ruta)

def mostrar_archivos(dialog, tipo, entity):
    """
    Displays the file list UI for a given entity.
    :param tipo: 'alumno' or 'asociacion'
    :param entity: Object representing the entity
    """
    dialog.clear()
    archivos = Archivo.obtener_archivos(tipo, entity.id)
    
    with dialog:
        with ui.card():
            ui.label(f"Expediente de {entity.nombre}")
            if not archivos:
                ui.label("Aún no hay archivos para esta entidad.")
            else:
                for archivo in archivos:
                    with ui.row():
                        ui.label(archivo.nombre_archivo)
                        ui.button("Abrir", on_click=lambda r=archivo.ruta_archivo: abrir_archivo(r))
                        ui.button("Eliminar", on_click=lambda a=archivo.id: eliminar_archivo(dialog, a, tipo, entity))
            subir_archivo_ui(dialog, tipo, entity)
    dialog.open()

def administrar_graficos(dialog):
    """
    Displays the UI for managing graficos, allowing users to upload a new Excel file to create a Grafico
    and delete existing ones.
    """
    dialog.clear()
    graficos = Grafico.obtener_graficos()

    with dialog:
        with ui.card():
            ui.label("Gestión de Gráficos")

            # Upload section
            with ui.row():
                ui.upload(
                    label="Subir Excel",
                    auto_upload=True,
                    on_upload=lambda file: agregar_grafico(dialog, file)
                )

            ui.separator()
            ui.markdown("### Gráficos Existentes")

            if not graficos:
                ui.label("No hay gráficos registrados.")
            else:
                for grafico in graficos:
                    with ui.row():
                        ui.label(f"{grafico.nombre} ({grafico.tipo})")
                        if grafico.archivo:
                            ui.button("Abrir", on_click=lambda r=grafico.archivo.ruta_archivo: abrir_archivo(r))
                            ui.button("Eliminar", on_click=lambda g=grafico.id: eliminar_grafico(dialog, g))

    dialog.open()

def agregar_grafico(dialog, file):
    """
    Handles the upload of an Excel file to create a new Grafico entry.
    Ensures that each Grafico has only one file.
    """
    session = obtener_sesion()
    try:
        # Create a new Grafico entry
        nuevo_grafico = Grafico(nombre=file.name, tipo="base")
        session.add(nuevo_grafico)
        session.commit()
        
        # Save the uploaded file and associate it with the Grafico
        Archivo.agregar_archivo(
            tipo='grafico',
            entity_id=nuevo_grafico.id,
            nombre_archivo=file.name,
            contenido=file.content.read()
        )
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    
    administrar_graficos(dialog)

def eliminar_grafico(dialog, grafico_id):
    """
    Deletes a Grafico entry and its associated file.
    :param grafico_id: ID of the grafico to delete
    """
    Grafico.eliminar_grafico(grafico_id)
    administrar_graficos(dialog)
