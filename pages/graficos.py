import os
import theme
from nicegui import ui
from models.grafico import Grafico
from utils.file_upload import administrar_graficos

def render_page():
    with theme.frame('Gráficos'):
        ui.page_title('Gráficos')
        ui.markdown('# Administración de Gráficos')

        # Upload new gráfico section
        with ui.card():
            ui.label("Subir nuevo gráfico")
            ui.upload(
                label="Subir Archivo de Gráfico (Excel)",
                auto_upload=True,
                on_upload=lambda file: agregar_nuevo_grafico(file)
            )

        ui.separator()

        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.markdown("## Lista de Gráficos")
            ui.input(
                placeholder="Buscar por nombre...",
                on_change=lambda e: actualizar_lista(e.value)
            )

        lista = ui.column()
        graficos_dialog = ui.dialog()

        def actualizar_lista(filtro=""):
            lista.clear()
            graficos = Grafico.obtener_graficos()
            graficos_filtrados = [g for g in graficos if filtro.lower() in g.nombre.lower()]

            for grafico in graficos_filtrados:
                with lista:
                    with ui.row():
                        ui.label(f"{grafico.id} - {grafico.nombre}, {grafico.tipo}")
                        ui.button("Ver Archivos", on_click=lambda g=grafico: administrar_graficos(graficos_dialog))
                        ui.button("Eliminar", color="red", on_click=lambda g=grafico: eliminar_grafico(g.id))

        def agregar_nuevo_grafico(file):
            """
            Handles file upload and creates a new gráfico entry.
            """
            ui.notify(f"Subiendo gráfico: {file.name}", color="blue")
            from utils.file_upload import agregar_grafico
            agregar_grafico(graficos_dialog, file)
            actualizar_lista()

        def eliminar_grafico(grafico_id):
            """
            Deletes a gráfico and updates the UI.
            """
            Grafico.eliminar_grafico(grafico_id)
            actualizar_lista()

        actualizar_lista()
