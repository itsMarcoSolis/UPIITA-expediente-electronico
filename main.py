import all_pages
import home_page
import theme

from nicegui import app, ui

from database import Base, engine

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)


# here we use our custom page decorator directly and just put the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()


# this call shows that you can also move the whole page creation into a separate file
all_pages.create()


ui.run(title='Expediente electrónico -')
