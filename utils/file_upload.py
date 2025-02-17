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
        label="📤 Subir nuevo archivo",
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
        pass
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
        pass
    else:
        mostrar_archivos(dialog, tipo, entity)

def abrir_archivo(ruta):
    """
    Opens a file with the default system program.
    If no application is associated, shows an error popup.
    """
    try:
        os.startfile(ruta)
    except OSError as e:
        ui.notify(f"❌ No se puede abrir el archivo.\n{str(e)}", color="red", position="top", duration=5)


def mostrar_archivos(dialog, tipo, entity):
    """
    Displays the file list UI for a given entity in an improved, more spacious dialog.
    :param tipo: 'alumno', 'asociacion', or 'grafico'
    :param entity: Object representing the entity
    """
    dialog.clear()
    archivos = Archivo.obtener_archivos(tipo, entity.id)

    with dialog:
        with ui.card().classes("w-2/3 max-w-3xl p-6"):
            ui.label(f"📁 Expediente de {entity.nombre}").classes("text-xl font-bold mb-2")

            if not archivos:
                ui.label("Aún no hay archivos para esta entidad.").classes("text-gray-500 italic mb-4")
            else:
                with ui.column().classes("max-h-80 overflow-auto w-full"):
                    for archivo in archivos:
                        with ui.row().classes("justify-between items-center w-full p-2 border-b"):
                            ui.label(archivo.nombre_archivo).classes("flex-grow text-sm")
                            with ui.row():
                                ui.button(icon="folder_open", on_click=lambda r=archivo.ruta_archivo: abrir_archivo(r)).props("flat round color=blue")
                                ui.button(icon="delete", on_click=lambda a=archivo.id: eliminar_archivo(dialog, a, tipo, entity)).props("flat round color=red")

            ui.separator()

            # Upload section
            with ui.column().classes("items-center w-full mt-2"):
                subir_archivo_ui(dialog, tipo, entity)
                # Close Button
                ui.button("Cerrar", icon="close", color="red-600", on_click=dialog.close).classes("mt-4 w-1/4")

    dialog.open()


def administrar_graficos():
    """
    Displays the UI for managing graficos, allowing users to upload a new Excel file to create a Grafico
    and delete existing ones.
    """
    graficos = Grafico.obtener_graficos()

    with ui.card():
        ui.label("Gestión de Gráficos")

        # Upload section
        with ui.row():
            ui.upload(
                label="Subir Excel",
                auto_upload=True,
                on_upload=lambda file: agregar_grafico( file)
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
                        ui.button("Eliminar", on_click=lambda g=grafico.id: eliminar_grafico(g))


def agregar_grafico(file):
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
    
def eliminar_grafico(grafico_id):
    """
    Deletes a Grafico entry and its associated file.
    :param grafico_id: ID of the grafico to delete
    """
    Grafico.eliminar_grafico(grafico_id)
