from nicegui import ui
import pages.alumnos
import pages.asociaciones

def create() -> None:
    ui.page('/alumnos/')(pages.alumnos.render_page)
    ui.page('/asociaciones/')(pages.asociaciones.render_page)

if __name__ == '__main__':
    create()
