import os
import theme
from nicegui import ui
from models.alumno import Alumno
from utils.file_upload import mostrar_archivos

CARRERAS = ["Biónica", "Energía", "ISISA", "Mecatrónica", "Telemática"]

def render_page():
    with theme.frame('Alumnos'):
        ui.page_title('Alumnos')
        ui.markdown('# 📚 Gestión de Alumnos')

        # ✅ Collapsible Form for Adding New Student
        with ui.expansion("Agregar nuevo alumno", icon="person_add").classes("w-full"):
            with ui.card().classes("w-full"):
                with ui.row().classes("items-center justify-between w-full"):
                    boleta = ui.input("Boleta").classes("w-1/5")
                    nombre = ui.input("Nombre").classes("w-1/5")
                    correo = ui.input("Correo electrónico").classes("w-1/5")
                    carrera = ui.select(CARRERAS, label="Carrera", value="Biónica").classes("w-1/5")
                with ui.row().classes("items-center justify-center w-full"):
                    ui.button("Agregar", on_click=lambda: [
                        Alumno.agregar_alumno(boleta.value, nombre.value, correo.value, carrera.value),
                        actualizar_lista()
                    ]).classes("w-1/4")


        ui.separator()
        
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.markdown("## Lista de Alumnos")
            ui.input(placeholder="Buscar por boleta o nombre...", on_change=lambda e: actualizar_lista(e.value))


        lista = ui.column()

        expediente_dialog = ui.dialog()

        def actualizar_lista(filtro=""):
            lista.clear()
            alumnos = Alumno.obtener_alumnos()
            alumnos_filtrados = [a for a in alumnos if filtro.lower() in a.boleta.lower() or filtro.lower() in a.nombre.lower()]
            
            for alumno in alumnos_filtrados:
                with lista:
                    with ui.row():
                        ui.label(f"{alumno.id} - {alumno.boleta}, {alumno.nombre}, {alumno.correo}, {alumno.carrera}")
                        ui.button("Ver Archivos", on_click=lambda a=alumno: mostrar_archivos(expediente_dialog, "alumno", a))
                        ui.button("Editar", on_click=lambda a=alumno: editar_alumno(a))

        def editar_alumno(alumno: Alumno):
            edit_dialog = ui.dialog()
            with edit_dialog:
                with ui.card():
                    ui.label(f"Editar Alumno: {alumno.nombre}")
                    new_boleta = ui.input("Boleta", value=alumno.boleta)
                    new_nombre = ui.input("Nombre", value=alumno.nombre)
                    new_correo = ui.input("Correo Electrónico", value=alumno.correo)
                    new_carrera = ui.select(CARRERAS, label="Carrera", value=alumno.carrera)
                    ui.button("Guardar Cambios", on_click=lambda: guardar_edicion(alumno.id, new_boleta.value, new_nombre.value, new_correo.value, new_carrera.value, edit_dialog))
            edit_dialog.open()

        def guardar_edicion(alumno_id, new_boleta, new_nombre, new_correo, new_carrera, dialog):
            Alumno.editar_alumno(alumno_id, new_boleta, new_nombre, new_correo, new_carrera)
            dialog.close()
            actualizar_lista()
        
        actualizar_lista()