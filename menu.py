from nicegui import ui


def menu() -> None:
    ui.link('Inicio', '/').classes(replace='text-black')
    ui.link('Alumnos', '/alumnos/').classes(replace='text-black')
    ui.link('Expedientes', '/asociaciones/').classes(replace='text-black')
    ui.link('Asociaciones', '/asociaciones/').classes(replace='text-black')
    ui.link('Gráficos', '/youtube-script/').classes(replace='text-black')
    ui.link('Cerrar sesión', '/youtube-script/').classes(replace='text-black')
