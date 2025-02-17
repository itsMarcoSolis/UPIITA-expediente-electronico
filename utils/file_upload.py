import os
from nicegui import ui
from models.archivo import Archivo
"""
    dialog parameter passed to the functions here has to be 
    initialized on the page context.
"""

def subir_archivo_ui(dialog, tipo, entity_id):
    """
    Creates an upload UI for files related to an Alumno or Asociacion.
    :param tipo: 'alumno' or 'asociacion'
    :param entity_id: ID of the associated entity
    """
    ui.upload(
        label="Subir Archivo",
        auto_upload=True,
        on_upload=lambda file: agregar_archivo(dialog, file, tipo, entity_id)
    )

def agregar_archivo(dialog, file, tipo, entity_id):
    """
    Saves the uploaded file and associates it with an entity.
    :param file: Uploaded file object
    :param tipo: 'alumno' or 'asociacion'
    :param entity_id: ID of the associated entity
    """
    Archivo.agregar_archivo(file.name, file.content.read(), tipo, entity_id)
    mostrar_archivos(dialog, tipo, entity_id)

def eliminar_archivo(dialog, archivo_id, tipo, entity_id):
    """
    Deletes a file from storage and database.
    :param archivo_id: ID of the file to delete
    :param tipo: 'alumno' or 'asociacion'
    :param entity_id: ID of the associated entity
    """
    Archivo.eliminar_archivo(archivo_id)
    mostrar_archivos(dialog, tipo, entity_id)

def abrir_archivo(ruta):
    """
    Opens a file with the default system program.
    :param ruta: Path to the file
    """
    os.startfile(ruta)


def mostrar_archivos(dialog, tipo, entity_id):
    """
    Displays the file list UI for a given entity.
    :param tipo: 'alumno' or 'asociacion'
    :param entity_id: ID of the associated entity
    """
    dialog.clear()
    archivos = Archivo.obtener_archivos(tipo, entity_id)
    entity_label = "Alumno" if tipo == "alumno" else "Asociación"
    with dialog:
        with ui.card():
            ui.label(f"Archivos de {entity_label} {entity_id}")
            if not archivos:
                ui.label("Aún no hay archivos para esta entidad.")
            else:
                for archivo in archivos:
                    with ui.row():
                        ui.label(archivo.nombre_archivo)
                        ui.button("Abrir", on_click=lambda r=archivo.ruta_archivo: abrir_archivo(r))
                        ui.button("Eliminar", on_click=lambda a=archivo.id: eliminar_archivo(dialog, a, tipo, entity_id))
            subir_archivo_ui(dialog, tipo, entity_id)
    dialog.open()