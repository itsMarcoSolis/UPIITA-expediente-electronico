import theme
from nicegui import ui, app
from models.asociacion import Asociacion
from models.grupo import Grupo
from models.miembro_asociacion import MiembroAsociacion
from models.alumno import Alumno
from models.miembro_grupo import MiembroGrupo
from utils.file_upload import mostrar_archivos

def render_page():
    with theme.frame('Asociaciones'):
        ui.page_title('Asociaciones')
        ui.markdown('# 🏛️ Gestión de Asociaciones')

        # ✅ Collapsible Form for Adding a New Association
        with ui.expansion("Agregar nueva asociación", icon="group_add").classes("w-full"):
            with ui.card().classes("w-full"):
                with ui.row().classes("items-center justify-between w-full"):
                    nombre = ui.input("Nombre de la asociación").classes("w-1/3")
                    asesor = ui.input("Asesor responsable").classes("w-1/3")
                with ui.row().classes("items-center justify-center w-full mt-2"):
                    ui.button("Registrar", on_click=lambda: [
                        Asociacion.agregar_asociacion(nombre.value, asesor.value),
                        actualizar_lista()
                    ]).classes("w-1/4")

        ui.separator()

        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.markdown("## Asociaciones Registradas")
            ui.input(placeholder="🔍 Buscar por nombre...", on_change=lambda e: actualizar_lista(e.value)).classes("w-1/3")

        lista = ui.column().classes("w-full")
        expediente_dialog = ui.dialog()

        def actualizar_lista(filtro="", open_asociacion = {}, open_grupos = {}):
            lista.clear()
            asociaciones = Asociacion.obtener_asociaciones()
            asociaciones_filtradas = [a for a in asociaciones if filtro.lower() in a.nombre.lower()]

            if not asociaciones_filtradas:
                with lista:
                    ui.label("No se encontraron asociaciones.").classes("text-gray-500 italic self-start")

            for asociacion in asociaciones_filtradas:
                with lista:
                    with ui.card().classes("w-full shadow-md p-4"):
                        # 📌 Association Header
                        with ui.row().classes("items-center justify-between").classes("w-full"):
                            with ui.row():
                                ui.label(f"📌 {asociacion.nombre}").classes("font-bold text-lg")
                                ui.label(f"👨‍🏫 Asesor: {asociacion.asesor}").classes("text-gray-500")
                            ui.button("📂 Ver Expediente", on_click=lambda a=asociacion: mostrar_archivos(expediente_dialog, "asociacion", a))
                        def toggle_expansion_asociacion(asociacion_id, value):
                                    open_asociacion[asociacion_id] = value  # Store the expansion state
                        # 📌 Members Section (Collapsible)
                        with ui.expansion("👥 Miembros", value=open_asociacion.get(asociacion.id, False), on_value_change=lambda e: toggle_expansion_asociacion(asociacion.id, e.value)).classes("mt-2 w-full"):
                            with ui.column().classes("ml-4 w-full"):

                                # Member List (With Conditional Handling)
                                miembros = MiembroAsociacion.obtener_miembros_por_asociacion(asociacion.id)
                                if not miembros:
                                    ui.label("No hay miembros en esta asociación.").classes("text-gray-500 italic self-start")
                                else:
                                    for miembro in miembros:
                                        with ui.row().classes("items-center justify-between w-full border-b py-2"):
                                            ui.label(f"{miembro.alumno.boleta} - {miembro.alumno.nombre}").classes("text-lg")
                                            ui.button("➖ Quitar", color="red-600", on_click=lambda m=miembro: [
                                                MiembroAsociacion.eliminar_miembro(m.id),
                                                actualizar_lista(open_asociacion=open_asociacion, open_grupos=open_grupos)
                                            ]).classes("ml-2 w-1/12")
                                
                                # Add New Member Section
                                with ui.row().classes("items-center justify-between w-full"):
                                    estudiantes = Alumno.obtener_alumnos()
                                    opciones_estudiantes = {a.id: f"{a.boleta} - {a.nombre}" for a in estudiantes}

                                    ui.select(opciones_estudiantes, label="Seleccionar estudiante a agregar", with_input=True).bind_value_to(
                                        asociacion, 'nuevo_miembro'
                                    ).classes("w-10/12")
                                    
                                    ui.button("👤➕ Agregar", on_click=lambda a=asociacion: [
                                        MiembroAsociacion.agregar_miembro(a.nuevo_miembro, a.id),
                                        actualizar_lista(open_asociacion=open_asociacion, open_grupos=open_grupos)
                                    ]).classes("ml-2 w-1/12")

                        ui.separator()
                        

                        def toggle_expansion(grupo_id, value):
                                    open_grupos[grupo_id] = value  # Store the expansion state
                        # 📌 Groups Section (Collapsible)
                        with ui.expansion("📂 Grupos", value=open_grupos.get(f"main-{asociacion.id}", False), on_value_change=lambda e: toggle_expansion("main", e.value)).classes("mt-2 w-full"):
                            with ui.column().classes("ml-4 w-full"):
                                # 🔄 List Existing Groups
                                grupos = Grupo.obtener_grupos_por_asociacion(asociacion.id)
                                if not grupos:
                                    ui.label("No hay grupos registrados.").classes("text-gray-500 italic self-start")
                                else:
                                    for grupo in grupos:
                                        with ui.row().classes("items-center justify-between w-full border-b py-2"):
                                                ui.label(f"{grupo.nombre_grupo}").classes("text-lg")
                                                ui.button("➖ Quitar", color="red-600", on_click=lambda g=grupo: [
                                                    Grupo.eliminar_grupo(g.id),
                                                    actualizar_lista(open_asociacion=open_asociacion, open_grupos=open_grupos)
                                                ]).classes("ml-2 w-1/12")
                                        # 👥 Members in Group (Collapsible)
                                        with ui.expansion(f"👤 Miembros del Grupo", value=open_grupos.get(grupo.id, False), on_value_change=lambda e: toggle_expansion(grupo.id, e.value)).classes("ml-4 w-full"):
                                            miembros = MiembroGrupo.obtener_miembros_grupo(grupo.id)
                                            
                                            if not miembros:
                                                ui.label("No hay miembros en este grupo.").classes("text-gray-500 italic self-start")
                                            else:
                                                for miembro in miembros:
                                                    with ui.row().classes("items-center justify-between w-full border-b py-2"):
                                                        ui.label(f"{miembro.alumno.boleta} - {miembro.alumno.nombre}").classes("text-lg")
                                                        ui.button("➖ Quitar", color="red-600", on_click=lambda m=miembro: [
                                                            MiembroGrupo.eliminar_miembro_grupo(m.id),
                                                            actualizar_lista(open_asociacion=open_asociacion, open_grupos=open_grupos)
                                                        ]).classes("ml-2 w-1/12")
                                            # ✅ Add Member to group Section 
                                            with ui.row().classes("items-center justify-between w-full"):
                                                estudiantes = Alumno.obtener_alumnos()
                                                opciones_estudiantes = {a.id: f"{a.boleta} - {a.nombre}" for a in estudiantes}

                                                ui.select(opciones_estudiantes, label="Seleccionar estudiante a agregar", with_input=True).bind_value_to(
                                                    grupo, 'nuevo_miembro'
                                                ).classes("w-10/12")
                                                
                                                ui.button("👤➕ Agregar", on_click=lambda a=asociacion, g=grupo: [
                                                    # Check if the student is already in the association
                                                    MiembroAsociacion.agregar_miembro(g.nuevo_miembro, a.id)
                                                    if g.nuevo_miembro not in {m.alumno_id for m in MiembroAsociacion.obtener_miembros_por_asociacion(a.id)}
                                                    else None,
                                                    
                                                    # Always add the student to the group
                                                    MiembroGrupo.agregar_miembro_grupo(g.nuevo_miembro, g.id),

                                                    # Refresh UI
                                                    actualizar_lista(open_asociacion=open_asociacion, open_grupos=open_grupos)
                                                ]).classes("ml-2 w-1/12")

                                # 🏷️ Add New Group (Now Inside the Expansion)
                                with ui.row().classes("items-center justify-between w-full"):
                                    nuevo_grupo = ui.input("Nuevo grupo").bind_value_to(asociacion, 'nuevo_grupo').classes("w-10/12")
                                    ui.button("➕ Agregar", on_click=lambda a=asociacion: [
                                        Grupo.agregar_grupo(a.id, a.nuevo_grupo),
                                        actualizar_lista(open_asociacion=open_asociacion, open_grupos=open_grupos)
                                    ]).classes("ml-2 w-1/12")


        actualizar_lista()
