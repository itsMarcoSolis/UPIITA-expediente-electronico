from contextlib import contextmanager

from menu import menu

from nicegui import ui


@contextmanager
def frame(navtitle: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary='#6C1D45', secondary='#8C1858', accent='#F2DCEB', positive='#53B689')
    with ui.column().classes('absolute-center items-center h-screen no-wrap p-9 w-full'):
        yield
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        ui.label('UPIITA - Expediente electrónico').classes('font-bold')

    with ui.footer(value=False) as footer:
        ui.label('Footer')
    with ui.left_drawer().classes('bg-amber-50') as left_drawer:
        with ui.column():
            menu()
    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle, icon='contact_support').props('fab')
