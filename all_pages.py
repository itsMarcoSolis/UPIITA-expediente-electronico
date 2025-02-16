from nicegui import ui
from pages.alumnos import render_page
from pages.asociaciones import script_generator

def create() -> None:
    ui.page('/alumnos/')(render_page)
    ui.page('/asociaciones/')(script_generator)

if __name__ == '__main__':
    create()
