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
        expediente_dialog = ui.dialog()
        def actualizar_lista():
            lista.clear()
            for asociacion in Asociacion.obtener_asociaciones():
                with lista:
                    with ui.card().classes('w-full'):
                        # Association header
                        with ui.row().classes('items-center'):
                            ui.label(f"{asociacion.nombre} - Asesor: {asociacion.asesor}")

                            # Add "View Files" Button
                            ui.button("Ver Archivos", on_click=lambda a=asociacion: mostrar_archivos(expediente_dialog, "asociacion", a.id))

                        # Add Group Section
                        with ui.input("Nuevo grupo").bind_value_to(
                            asociacion, 'nuevo_grupo').classes('w-48'):
                            ui.tooltip("Nombre del nuevo grupo")
                        ui.button(icon='add', on_click=lambda a=asociacion: [
                            Grupo.agregar_grupo(a.id, a.nuevo_grupo),
                            actualizar_lista()
                        ])
                        
                        # Members management section
                        with ui.column().classes('ml-8'):
                            ui.markdown("### Miembros")
                            
                            # Add Member Section
                            with ui.row().classes('items-center'):
                                estudiantes = Alumno.obtener_alumnos()
                                opciones_estudiantes = {a.id: f"{a.boleta} - {a.nombre}" for a in estudiantes}
                                
                                ui.select(opciones_estudiantes, label="Seleccionar estudiante").bind_value_to(
                                    asociacion, 'nuevo_miembro').classes('w-64')
                                ui.button(icon='person_add', on_click=lambda a=asociacion: [
                                    MiembroAsociacion.agregar_miembro(a.nuevo_miembro, a.id),
                                    actualizar_lista()
                                ])
                            
                            # Current members list
                            with ui.column().classes('ml-4'):
                                for miembro in MiembroAsociacion.obtener_miembros_por_asociacion(asociacion.id):
                                    with ui.row().classes('items-center'):
                                        # Access alumno through the already loaded relationship
                                        ui.label(f"{miembro.alumno.boleta} - {miembro.alumno.nombre}")
                                        ui.button(icon='person_remove', color='red', on_click=lambda m=miembro: [
                                            MiembroAsociacion.eliminar_miembro(m.id),
                                            actualizar_lista()
                                        ]).classes('ml-2')
                        
                        # List of groups with edit/delete
                        with ui.column().classes('ml-8'):
                            for grupo in Grupo.obtener_grupos_por_asociacion(asociacion.id):
                                with ui.row().classes('items-center'):
                                    # Editable field with proper state management
                                    edit_state = app.storage.general.get(f'edit_{grupo.id}', False)
                                    input = None
                                    
                                    if not edit_state:
                                        ui.label(grupo.nombre_grupo)
                                    else:
                                        input = ui.input(value=grupo.nombre_grupo).classes('w-32')
                                    
                                    with ui.row():
                                        # Edit/Save toggle
                                        if not edit_state:
                                            ui.button(icon='edit', on_click=lambda g=grupo: [
                                                app.storage.general.update({f'edit_{g.id}': True}),
                                                actualizar_lista()
                                            ])
                                        else:
                                            ui.button(icon='save', on_click=lambda g=grupo, i=input: [
                                                Grupo.actualizar_grupo(g.id, i.value),
                                                app.storage.general.update({f'edit_{g.id}': False}),
                                                actualizar_lista()
                                            ])
                                        
                                        # Delete button
                                        ui.button(icon='delete', color='red', on_click=lambda g=grupo: [
                                            Grupo.eliminar_grupo(g.id),
                                            app.storage.general.pop(f'edit_{g.id}', None),
                                            actualizar_lista()
                                        ])
                                    with ui.column().classes('ml-12'):  # Increased indentation
                                        ui.markdown("#### Miembros del Grupo")
                                        
                                        # Add member to group
                                        with ui.row().classes('items-center'):
                                            estudiantes = Alumno.obtener_alumnos()
                                            opciones_estudiantes = {a.id: f"{a.boleta} - {a.nombre}" for a in estudiantes}
                                            
                                            ui.select(opciones_estudiantes, label="Agregar estudiante").bind_value_to(
                                                grupo, 'nuevo_miembro').classes('w-64')
                                            ui.button(icon='person_add', on_click=lambda g=grupo: [
                                                MiembroGrupo.agregar_miembro_grupo(g.nuevo_miembro, g.id),
                                                actualizar_lista()
                                            ])
                                        
                                        # List current group members
                                        with ui.column().classes('ml-4'):
                                            for miembro in MiembroGrupo.obtener_miembros_grupo(grupo.id):
                                                with ui.row().classes('items-center'):
                                                    ui.label(f"{miembro.alumno.boleta} - {miembro.alumno.nombre} ({miembro.fecha_ingreso.strftime('%d/%m/%Y')})")
                                                    ui.button(icon='person_remove', color='red', on_click=lambda m=miembro: [
                                                        MiembroGrupo.eliminar_miembro_grupo(m.id),
                                                        actualizar_lista()
                                                    ]).classes('ml-2')
        actualizar_lista()
