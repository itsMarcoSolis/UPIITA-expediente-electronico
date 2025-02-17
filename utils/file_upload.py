import os
from nicegui import ui
from models.archivo import Archivo

"""
    dialog parameter passed to the functions here has to be 
    initialized on the page context.
"""

def subir_archivo_ui(dialog, tipo, entity):
    """
    Creates an upload UI for files related to an Alumno or Asociacion.
    :param tipo: 'alumno' or 'asociacion'
    :param entity.id: ID of the associated entity
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
    :param tipo: 'alumno' or 'asociacion'
    :param entity.id: ID of the associated entity
    """
    # Check if the file already exists for this entity
    archivos_existentes = Archivo.obtener_archivos(tipo, entity.id)
    if any(archivo.nombre_archivo == file.name for archivo in archivos_existentes):
        ui.notify(f"El archivo '{file.name}' ya existe en este {tipo}.", color="red")
        return
    
    # Save the file if it's not a duplicate
    Archivo.agregar_archivo(file.name, file.content.read(), tipo, entity.id)
    mostrar_archivos(dialog, tipo, entity)

def eliminar_archivo(dialog, archivo_id, tipo, entity):
    """
    Deletes a file from storage and database.
    :param archivo_id: ID of the file to delete
    :param tipo: 'alumno' or 'asociacion'
    :param entity.id: ID of the associated entity
    """
    Archivo.eliminar_archivo(archivo_id)
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
    :param entity.id: ID of the associated entity
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
