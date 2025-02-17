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
            carrera = ui.select(["Biónica", "Energía", "Mecatrónica", "Telemática"], label="Carrera", value="Biónica")
            ui.button("Agregar", on_click=lambda: [
                Alumno.agregar_alumno(boleta.value, nombre.value, correo.value, carrera.value),
                actualizar_lista()
            ])

        ui.separator()
        
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.markdown("## Lista de Alumnos")
            ui.input(placeholder="Buscar por boleta o nombre...", on_change=lambda e: actualizar_lista(e.value))

        lista = ui.column()

        def actualizar_lista(filtro=""):
            lista.clear()
            alumnos = Alumno.obtener_alumnos()
            alumnos_filtrados = [a for a in alumnos if filtro.lower() in a.boleta.lower() or filtro.lower() in a.nombre.lower()]
            
            for alumno in alumnos_filtrados:
                with lista:
                    with ui.row():
                        ui.label(f"{alumno.id} - {alumno.boleta}, {alumno.nombre}, {alumno.correo}, {alumno.carrera}")
                        ui.button("Ver Archivos", on_click=lambda a=alumno: mostrar_archivos(a))
                        ui.button("Editar", on_click=lambda a=alumno: editar_alumno(a))

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

        def editar_alumno(alumno: Alumno):
            edit_dialog = ui.dialog()
            with edit_dialog:
                with ui.card():
                    ui.label(f"Editar Alumno: {alumno.nombre}")
                    new_boleta = ui.input("Boleta", value=alumno.boleta)
                    new_nombre = ui.input("Nombre", value=alumno.nombre)
                    new_correo = ui.input("Correo Electrónico", value=alumno.correo)
                    new_carrera = ui.select(["Mecatrónica", "Telemática", "Biónica", "Energía"], label="Carrera", value=alumno.carrera)
                    ui.button("Guardar Cambios", on_click=lambda: guardar_edicion(alumno.id, new_boleta.value, new_nombre.value, new_correo.value, new_carrera.value, edit_dialog))
            edit_dialog.open()

        def guardar_edicion(alumno_id, new_boleta, new_nombre, new_correo, new_carrera, dialog):
            Alumno.editar_alumno(alumno_id, new_boleta, new_nombre, new_correo, new_carrera)
            dialog.close()
            actualizar_lista()
        
        actualizar_lista()