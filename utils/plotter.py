import pandas as pd
from nicegui import ui
from models.grafico import Grafico

grafico_container = None  # Store reference to keep UI clean

def display_grafico(grafico):
    """
    Reads an Excel file, extracts sheet names, and allows selection.
    Ensures only one UI container exists at a time.
    """
    global grafico_container  # Track the currently displayed graphic

    # Remove the previous container if it exists
    if grafico_container:
        grafico_container.clear()
        grafico_container.delete()  # Fully delete old UI

    # Create new container
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
        """ Updates the selected sheet and refreshes UI. """
        selected_sheet["name"] = sheet_name
        actualizar_info()

    def actualizar_info():
        """ Clears and updates the UI with sheet selection. """
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
    return grafico_container  # Always return the active container

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
        elif "materia" in df.columns:
            sheet_type = "disponibilidad"

        # Step 2: Process based on sheet type
        if sheet_type == "inscritos_por_carrera":
            process_inscritos_por_carrera(df, container)
        elif sheet_type == "disponibilidad":
            process_disponibilidad(df, container)
        else:
            with container:
                ui.label(f"Tipo de hoja no identificado: {sheet_name}").classes("text-yellow-500")

    except Exception as e:
        ui.label(f"Error al procesar la hoja: {str(e)}").classes("text-red-500")

def process_disponibilidad(df, container):
    """
    Processes a sheet that follows the 'disponibilidad' format and generates a table with progress bars inside aggrid.
    """

    # Filter only relevant columns
    required_columns = ["grupo", "materia", "nombre de la materia", "semestre", "cupo", "inscritos", "disponibles"]
    df = df[[col for col in required_columns if col in df.columns]].copy()

    # Convert numeric columns to integers where possible
    for col in ["cupo", "inscritos", "disponibles"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Calculate occupied spots
    df["ocupacion"] = df["inscritos"]  # Now using "Inscritos" as the value

    # Prepare row data for aggrid
    row_data = []
    for _, row in df.iterrows():
        seats_taken = row["ocupacion"]  # Number of seats occupied
        total_capacity = row["cupo"]
        fill_ratio = (seats_taken / total_capacity) * 100 if total_capacity > 0 else 0  # Convert to percentage for bar width

        # Define colors dynamically based on how full the class is
        color = "#4caf50" if fill_ratio < 80 else "#f44336"  # Green if < 80% full, Red otherwise

        # Generate the progress bar with actual occupied seats
        progress_bar_html = f'''
            <div style="width: 100px; height: 15px; background: #ddd; border-radius: 5px; position: relative;">
                <div style="width: {fill_ratio:.1f}%; height: 100%; background: {color}; border-radius: 5px;"></div>
                <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                            font-size: 10px; font-weight: bold; color: black;">
                    {seats_taken} / {total_capacity}
                </span>
            </div>
        '''
        
        row_data.append({
            "Grupo": row["grupo"],
            "Materia": row["materia"],
            "Nombre de la Materia": row["nombre de la materia"],
            "Semestre": row["semestre"],
            "Cupo": row["cupo"],
            "Disponibilidad": progress_bar_html  # Store the HTML inside the field
        })

    # Create the aggrid UI
    with container:
        ui.aggrid({
            'defaultColDef': {'flex': 1},
            'columnDefs': [
                {'headerName': 'Grupo', 'field': 'Grupo'},
                {'headerName': 'Materia', 'field': 'Materia'},
                {'headerName': 'Nombre de la Materia', 'field': 'Nombre de la Materia'},
                {'headerName': 'Semestre', 'field': 'Semestre'},
                {'headerName': 'Cupo', 'field': 'Cupo'},
                {'headerName': 'Ocupabilidad', 'field': 'Disponibilidad'},
            ],
            'rowData': row_data,
            'rowSelection': 'single',
        }, html_columns=[5]).classes("")  # Enable HTML rendering in this column


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
