import os
import theme
from nicegui import ui
from models.alumno import Alumno
from models.archivo import Archivo


def abrir_archivo(ruta):
    os.startfile(ruta)

def render_page():
    with theme.frame('Alumnos'):
        ui.page_title('Alumnos')
        ui.markdown('# Esta es la página de alumnos!')

        with ui.card():
            ui.label("Agregar nuevo alumno")
            boleta = ui.input("Boleta")
            nombre = ui.input("Nombre")
            correo = ui.input("Correo electrónico")
            ui.button("Agregar", on_click=lambda: [
                Alumno.agregar_alumno(boleta.value, nombre.value, correo.value),
                actualizar_lista()
            ])

        ui.separator()
        ui.markdown("## Lista de Alumnos")
        lista = ui.column()

        def actualizar_lista():
            lista.clear()
            for alumno in Alumno.obtener_alumnos():
                with lista:
                    with ui.row():
                        ui.label(f"{alumno.id} - {alumno.boleta}, {alumno.nombre}, {alumno.correo}")
                        ui.button("Ver Archivos", on_click=lambda a=alumno: mostrar_archivos(a))

        dialog = ui.dialog()

        def mostrar_archivos(alumno: Alumno):
            dialog.clear()
            archivos = Archivo.obtener_archivos("alumno", alumno.id)
            
            with dialog:
                with ui.card():
                    ui.label(f"Archivos de {alumno.nombre}")
                    if not archivos:
                        ui.label("Aún no hay archivos en el expediente de este alumno.")
                    else:
                        for archivo in archivos:
                            with ui.row():
                                ui.label(archivo.nombre_archivo)
                                ui.button("Abrir", on_click=lambda r=archivo.ruta_archivo: abrir_archivo(r))
                                ui.button("Eliminar", on_click=lambda a=archivo.id: eliminar_archivo(a, alumno))
                    subir_archivo_ui(alumno)
            
            dialog.open()

        def subir_archivo_ui(alumno: Alumno):
            ui.upload(
                label="Subir Archivo",
                auto_upload=True,
                on_upload=lambda file: agregar_archivo(file, alumno)
            )

        def agregar_archivo(file, alumno: Alumno):
            Archivo.agregar_archivo(file.name, file.content.read(), "alumno", alumno.id)
            mostrar_archivos(alumno)

        def eliminar_archivo(archivo_id, alumno: Alumno):
            Archivo.eliminar_archivo(archivo_id)
            mostrar_archivos(alumno)
        
        actualizar_lista()
