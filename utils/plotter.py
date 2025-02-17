import pandas as pd
from nicegui import ui
from models.grafico import Grafico

# Store global container reference
grafico_container = None  

def display_grafico(grafico):
    """
    Reads an Excel file, extracts sheet names, and allows selection.
    Prevents multiple UI components from stacking by updating the existing container.

    :param grafico: Grafico object containing details
    """
    global grafico_container

    # Ensure we clear and reuse the same container
    if grafico_container:
        grafico_container.clear()
    else:
        grafico_container = ui.column().classes("mt-4 p-4 border border-gray-300 rounded-lg")

    # Attempt to read the file
    try:
        xls = pd.ExcelFile(grafico.archivo.ruta_archivo)  # Read Excel file
        sheet_names = xls.sheet_names  # Get sheet names
    except Exception as e:
        with grafico_container:
            ui.label(f"Error al leer el archivo: {str(e)}").classes("text-red-500")
        return grafico_container

    # State to track selected sheet (default to the first one)
    selected_sheet = {"name": sheet_names[0] if sheet_names else None}

    def set_selected_sheet(sheet_name):
        """
        Updates the selected sheet and refreshes UI.
        """
        selected_sheet["name"] = sheet_name
        actualizar_info()

    def actualizar_info():
        """
        Clears and updates the UI with sheet selection.
        """
        grafico_container.clear()
        with grafico_container:
            ui.label(f"{grafico.nombre}").classes("font-bold text-lg")

            if sheet_names:
                with ui.row():
                    for sheet in sheet_names:
                        ui.button(sheet, on_click=lambda s=sheet: set_selected_sheet(s)).classes(
                            "px-4 py-2 m-1 border rounded-lg"
                        )

                ui.label(f"📄 Hoja seleccionada: {selected_sheet['name']}").classes("mt-2 font-semibold")

    actualizar_info()  # Load UI initially
    return grafico_container
