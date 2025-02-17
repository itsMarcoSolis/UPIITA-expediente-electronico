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
                    ui.button("Agregar", icon="person_add", color="green", on_click=lambda: [
                        Alumno.agregar_alumno(boleta.value, nombre.value, correo.value, carrera.value),
                        actualizar_lista()
                    ]).classes("w-1/4")

        ui.separator()
        
        # ✅ Search Bar
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.markdown("## 📋 Lista de Alumnos")
            search_input = ui.input(placeholder="🔍 Buscar por boleta o nombre...", on_change=lambda e: actualizar_lista(e.value)).classes("w-1/3")

        lista = ui.column().classes("w-full")

        expediente_dialog = ui.dialog()

        def actualizar_lista(filtro=""):
            lista.clear()
            alumnos = Alumno.obtener_alumnos()
            alumnos_filtrados = [a for a in alumnos if filtro.lower() in a.boleta.lower() or filtro.lower() in a.nombre.lower()]

            if not alumnos_filtrados:
                with lista:
                    ui.label("No se encontraron alumnos.").classes("text-gray-500 italic")

            for alumno in alumnos_filtrados:
                with lista:
                    with ui.card().classes("w-full p-4 hover:bg-gray-100 transition-all rounded-lg"):
                        with ui.row().classes("justify-between items-center w-full"):
                            with ui.column():
                                ui.label(f"🎓 {alumno.nombre}").classes("font-semibold text-lg")
                                ui.label(f"📌 {alumno.boleta} | 📧 {alumno.correo} | 🏫 {alumno.carrera}").classes("text-gray-600 text-sm")
                            with ui.row():
                                ui.button("📂 Ver Expediente", color="blue", on_click=lambda a=alumno: mostrar_archivos(expediente_dialog, "alumno", a))
                                ui.button("✏️ Editar", color="orange", on_click=lambda a=alumno: editar_alumno(a))

        def editar_alumno(alumno: Alumno):
            edit_dialog = ui.dialog()
            with edit_dialog:
                with ui.card().classes("w-1/5 items-center"):
                    ui.label(f"✏️ Editar Alumno: {alumno.nombre}").classes("font-bold text-lg")
                    new_boleta = ui.input("Boleta", value=alumno.boleta).classes("w-8/12")
                    new_nombre = ui.input("Nombre", value=alumno.nombre).classes("w-8/12")
                    new_correo = ui.input("Correo Electrónico", value=alumno.correo).classes("w-8/12")
                    new_carrera = ui.select(CARRERAS, label="Carrera", value=alumno.carrera).classes("w-8/12")
                    ui.button("Guardar Cambios", color="green", icon="save", on_click=lambda: guardar_edicion(alumno.id, new_boleta.value, new_nombre.value, new_correo.value, new_carrera.value, edit_dialog))
            edit_dialog.open()

        def guardar_edicion(alumno_id, new_boleta, new_nombre, new_correo, new_carrera, dialog):
            Alumno.editar_alumno(alumno_id, new_boleta, new_nombre, new_correo, new_carrera)
            dialog.close()
            actualizar_lista()
        
        actualizar_lista()
