import all_pages
import home_page
import theme
import os
from utils.window_manager import WindowMgr, set_window_icon
from nicegui import app, ui

from database import Base, engine


FAVICON_PATH = os.path.join("static", "favicon.ico")
WINDOW_TITLE="UPIITA - Expediente electrónico"
set_window_icon(FAVICON_PATH, WINDOW_TITLE)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)


# here we use our custom page decorator directly and just put the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()


# this call shows that you can also move the whole page creation into a separate file
all_pages.create()

app.native.start_args['icon'] = FAVICON_PATH

ui.run(title=WINDOW_TITLE, favicon=FAVICON_PATH, native=True)
