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
        grafico_container = ui.column().classes("mt-4 p-4 border border-gray-300 rounded-lg w-full")

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

            # Process the selected sheet
            if selected_sheet["name"]:
                process_selected_sheet(xls, selected_sheet["name"], grafico_container)

    actualizar_info()  # Load UI initially
    return grafico_container

def process_selected_sheet(xls: pd.ExcelFile, sheet_name, container):
    """
    Reads the selected sheet, identifies its type, and processes it accordingly.
    """
    try:
        df = xls.parse(sheet_name)
        df.dropna(how="all", inplace=True)  # Remove fully empty rows
        df.columns = df.columns.str.strip().str.lower()  # Normalize column names
        
        # Step 1: Identify sheet type
        sheet_type = None
        if set(df.columns) >= {"nombre_carrera", "inscritos"}:
            sheet_type = "inscritos_por_carrera"

        # Step 2: Process based on sheet type
        if sheet_type == "inscritos_por_carrera":
            process_inscritos_por_carrera(df, container)
        
        else:
            with container:
                ui.label(f"Tipo de hoja no identificado: {sheet_name}").classes("text-yellow-500")

    except Exception as e:
        ui.label(f"Error al procesar la hoja: {str(e)}").classes("text-red-500")


def process_inscritos_por_carrera(df, container):
    """
    Processes a sheet that follows the 'inscritos_por_carrera' format and generates a bar chart.
    """
    df = df[["nombre_carrera", "inscritos"] + [col for col in ["plan_estud", "semestre"] if col in df.columns]].copy()

    # Identify rows where all columns except 'inscritos' are empty or NaN
    empty_except_inscritos = df.drop(columns=["inscritos"]).apply(lambda row: row.isna().all(), axis=1)

    # Normalize data using .loc[] to avoid SettingWithCopyWarning
    df.loc[:, "nombre_carrera"] = df["nombre_carrera"].astype(str).str.strip()
    # Explicitly convert to string to prevent dtype mismatches
    if "plan_estud" in df.columns:
        df["plan_estud"] = df["plan_estud"].astype("object")  # Force object dtype first
        df["plan_estud"] = df["plan_estud"].astype(str).str.replace(r"\.0$", "", regex=True)

    if "semestre" in df.columns:
        df["semestre"] = df["semestre"].astype("object")  # Force object dtype first
        df["semestre"] = df["semestre"].astype(str).str.replace(r"\.0$", "", regex=True)




    # Convert empty strings to NaN for consistency
    df.replace("", pd.NA, inplace=True)

    # Identify special rows
    total_row = df[df["nombre_carrera"].str.lower() == "total"]
    fecha_row = df[df["nombre_carrera"].str.lower().str.contains("fecha de corte", na=False)]
    corte_row = df[df["nombre_carrera"].str.lower().str.startswith("corte", na=False)]

    # Identify rows where all columns except 'inscritos' are NaN or empty


    # Filter valid data for the chart
    df_filtered = df[
        ~df["nombre_carrera"].str.lower().isin(["total"]) & 
        ~df["nombre_carrera"].str.lower().str.contains("fecha de corte", na=False) & 
        ~df["nombre_carrera"].str.lower().str.startswith("corte", na=False) & 
        ~empty_except_inscritos
    ]

    # Extract total value if present
    total_value = df.loc[empty_except_inscritos, "inscritos"].dropna().values
    total_value = total_value[0] if len(total_value) > 0 else None

    # Format labels for the x-axis
    labels = []
    for _, row in df_filtered.iterrows():
        label = row["nombre_carrera"]
        if "semestre" in df_filtered.columns and pd.notna(row["semestre"]):
            label += f", Semestre {row['semestre']}"
        elif "plan_estud" in df_filtered.columns and pd.notna(row["plan_estud"]):
            label += f", Plan {row['plan_estud']}"
        labels.append(label)

    # Generate bar chart
    with container:
        chart = ui.highchart({
            'title': False,
            'chart': {'type': 'bar'},
            'xAxis': {'categories': labels},
            'series': [{'name': 'Inscritos', 'data': df_filtered["inscritos"].tolist()}],
        }).classes('w-full h-64')

        # Display Total if exists
        if not total_row.empty:
            ui.label(f"Total: {total_row['inscritos'].values[0]}").classes("font-bold mt-2")

        # Display Fecha de Corte if exists
        if not fecha_row.empty:
            ui.label(f"Fecha de corte: {fecha_row['inscritos'].values[0]}").classes("italic mt-2")

        # Display Corte row if exists
        if not corte_row.empty:
            corte_label = f"{corte_row['nombre_carrera'].values[0]}"
            if len(corte_row.columns) > 1:  # Check if there's something in another column
                extra_value = corte_row.iloc[0, 1] if pd.notna(corte_row.iloc[0, 1]) else None
                inscritos_value = corte_row["inscritos"].values[0] if "inscritos" in corte_row else None

                if extra_value and not pd.isna(extra_value):
                    corte_label += f": {extra_value}"
                elif inscritos_value and not pd.isna(inscritos_value):
                    corte_label += f": {inscritos_value}"

            ui.label(corte_label).classes("italic mt-2")

        # Display case when only "inscritos" is populated
        if total_value:
            ui.label(f"Total: {total_value}").classes("font-bold mt-2")
