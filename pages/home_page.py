from nicegui import ui
import theme

def render_page():
    with theme.frame('Inicio'):
        ui.page_title("UPIITA Expediente Electrónico")

        # Hero Section
        with ui.column().classes("items-center justify-center text-center w-full mt-8"):
            ui.label("📚 Gestión Inteligente de Expedientes").classes("text-3xl font-bold")
            ui.label("Administra alumnos, asociaciones y gráficos en un solo lugar").classes("text-lg text-gray-500")
        ui.separator().classes("my-6 w-3/4 mx-auto")

        # Features Grid
        with ui.row().classes("gap-6 w-3/4 mx-auto justify-center"):
            feature_card("🎓", "Alumnos", "Administra la información de los estudiantes.", "/alumnos")
            feature_card("🏛", "Asociaciones", "Gestiona las asociaciones y sus miembros.", "/asociaciones")
            feature_card("📊", "Gráficos", "Analiza datos con reportes visuales interactivos.", "/graficos")

        # Footer
        with ui.row().classes("justify-center mt-10 text-sm text-gray-500"):
            ui.label("Desarrollado para UPIITA | 📌 Gestión eficiente y segura de datos")

def feature_card(icon, title, description, route):
    """Reusable card component for features."""
    with ui.card().classes("p-6 shadow-md hover:shadow-lg transition duration-300 cursor-pointer w-1/4 items-center"):
        with ui.column().classes("items-center text-center"):
            ui.label(icon).classes("text-4xl")
            ui.label(title).classes("text-xl font-semibold mt-2")
            ui.label(description).classes("text-sm text-gray-500 mt-1")
            ui.button("Explorar", on_click=lambda: ui.navigate.to(route)).classes("mt-3 w-full bg-blue-500 text-white rounded-lg hover:bg-blue-600")

