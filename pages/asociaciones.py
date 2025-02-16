# pages/asociaciones.py
import theme
from nicegui import ui
from models.asociacion import Asociacion

def render_page():
    with theme.frame('Asociaciones'):
        ui.page_title('Asociaciones')
        ui.markdown('# Gestión de Asociaciones')

        # Add Association Form
        with ui.card():
            ui.label("Nueva Asociación")
            nombre = ui.input("Nombre de la asociación")
            asesor = ui.input("Asesor responsable")
            ui.button("Registrar Asociación", 
                      on_click=lambda: [
                          Asociacion.agregar_asociacion(nombre.value, asesor.value),
                          actualizar_lista()
                      ])

        ui.separator()
        ui.markdown("## Asociaciones Registradas")
        lista = ui.column()

        # Dynamic List Update
        def actualizar_lista():
            lista.clear()
            for asociacion in Asociacion.obtener_asociaciones():
                with lista:
                    ui.label(f"{asociacion.id}: {asociacion.nombre} - Asesor: {asociacion.asesor}")
        
        actualizar_lista()