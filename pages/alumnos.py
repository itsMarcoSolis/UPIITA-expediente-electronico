import theme
from nicegui import ui
from models.alumno import Alumno

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
                    ui.label(f"{alumno.id} - {alumno.boleta}, {alumno.nombre}, {alumno.correo}")
        
        actualizar_lista()
