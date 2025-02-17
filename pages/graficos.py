import os
import theme
from nicegui import ui
from models.grafico import Grafico
from utils.plotter import display_grafico

def render_page():
    with theme.frame("Gráficos"):
        ui.page_title("Gráficos")
        ui.markdown("## 📊 Administración de Gráficos")

        # ✅ Upload Section with Card
        with ui.card().classes("w-full p-4"):
            ui.label("📂 Subir nuevo gráfico").classes("text-lg font-semibold")
            ui.upload(
                label="Seleccionar Archivo (Excel)",
                auto_upload=True,
                on_upload=lambda file: agregar_nuevo_grafico(file)
            ).classes("w-full")

        ui.separator()

        # ✅ Search & List Section
        with ui.row().classes("justify-between w-full items-center"):
            ui.markdown("### 📋 Lista de Gráficos").classes("text-lg font-semibold")
            ui.input(placeholder="🔎 Buscar gráfico...", on_change=lambda e: actualizar_lista(e.value)).classes("w-1/3")

        lista = ui.column().classes("w-full mt-2")
        grafico_display = None  # Placeholder for the selected gráfico

        def actualizar_lista(filtro=""):
            """ Updates the list of gráficos with the search filter applied. """
            lista.clear()
            graficos = Grafico.obtener_graficos()
            graficos_filtrados = [g for g in graficos if filtro.lower() in g.nombre.lower()]

            if not graficos_filtrados:
                ui.label("⚠️ No hay gráficos registrados. ¡Sube uno!").classes("text-gray-500 italic").classes("self-start")
                return

            for grafico in graficos_filtrados:
                with lista:
                    with ui.card().classes("w-full p-4 flex items-center justify-between"):
                        grafico_column = ui.column().classes("items-center")
                        with grafico_column:
                            ui.label(f"📊 {grafico.nombre}").classes("text-md font-semibold")

                            with ui.row().classes("gap-2"):
                                ui.button("👁️ Ver", on_click=lambda p=grafico_column, g=grafico: seleccionar_grafico(g,p)).props("outline")
                                ui.button("🗑️ Eliminar", color="red", on_click=lambda g=grafico: confirmar_eliminar_grafico(g)).props("outline")

        def seleccionar_grafico(grafico, parent):
            """ Updates the UI to show the selected gráfico's details. """
            nonlocal grafico_display
            if grafico_display:
                grafico_display.clear()
            with parent:
                grafico_display = display_grafico(grafico)

        def agregar_nuevo_grafico(file):
            """ Handles file upload and creates a new gráfico entry. """
            ui.notify(f"📤 Subiendo gráfico: {file.name}", color="blue")
            from utils.file_upload import agregar_grafico
            agregar_grafico(file)  # No dialog needed
            actualizar_lista()

        def confirmar_eliminar_grafico(grafico):
            """ Shows a confirmation dialog before deleting a gráfico. """
            with ui.dialog() as confirm_dialog:
                with ui.card():
                    ui.label(f"⚠️ ¿Eliminar '{grafico.nombre}'?").classes("text-red-600 text-lg font-bold")
                    ui.label("Esta acción no se puede deshacer.").classes("text-gray-500")

                    with ui.row().classes("justify-end mt-4"):
                        ui.button("Cancelar", on_click=confirm_dialog.close).props("outline")
                        ui.button("Eliminar", color="red", on_click=lambda g=grafico: eliminar_grafico(g)).props("outline")

            confirm_dialog.open()

        def eliminar_grafico(grafico):
            """ Deletes a gráfico and updates the UI. """
            Grafico.eliminar_grafico(grafico.id)
            ui.notify(f"✅ Gráfico '{grafico.nombre}' eliminado.", color="green")
            actualizar_lista()

        actualizar_lista()
