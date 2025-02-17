from nicegui import ui
import pages.alumnos
import pages.asociaciones
import pages.graficos

def create() -> None:
    ui.page('/alumnos/')(pages.alumnos.render_page)
    ui.page('/asociaciones/')(pages.asociaciones.render_page)
    ui.page('/graficos/')(pages.graficos.render_page)

if __name__ == '__main__':
    create()
