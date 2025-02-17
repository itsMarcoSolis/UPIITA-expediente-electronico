from nicegui import ui


def menu() -> None:
    ui.link('Inicio', '/').classes(replace='text-black')
    ui.link('Alumnos', '/alumnos/').classes(replace='text-black')
    ui.link('Asociaciones', '/asociaciones/').classes(replace='text-black')
    ui.link('Gráficos', '/graficos/').classes(replace='text-black')
