import os
import theme
from nicegui import ui
from models.grafico import Grafico
from utils.plotter import display_grafico

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

        with ui.row().classes("justify-between w-full"):
            ui.markdown("## Lista de Gráficos")
            ui.input(
                placeholder="Buscar por nombre...",
                on_change=lambda e: actualizar_lista(e.value)
            )

        lista = ui.column()
        grafico_display = None  # Placeholder for selected gráfico UI

        def actualizar_lista(filtro=""):
            lista.clear()
            graficos = Grafico.obtener_graficos()
            graficos_filtrados = [g for g in graficos if filtro.lower() in g.nombre.lower()]

            for grafico in graficos_filtrados:
                with lista:
                    ui.button(
                        f"{grafico.id} - {grafico.nombre}, {grafico.tipo}",
                        on_click=lambda g=grafico: seleccionar_grafico(g)
                    ).classes("w-full text-left")

        def seleccionar_grafico(grafico):
            """
            Updates the UI to show the selected gráfico's details.
            """
            nonlocal grafico_display
            if grafico_display:
                grafico_display.clear()

            grafico_display = display_grafico(grafico)

        def agregar_nuevo_grafico(file):
            """
            Handles file upload and creates a new gráfico entry.
            """
            ui.notify(f"Subiendo gráfico: {file.name}", color="blue")
            from utils.file_upload import agregar_grafico
            agregar_grafico(file)  # Passing None since there's no dialog
            actualizar_lista()

        actualizar_lista()
