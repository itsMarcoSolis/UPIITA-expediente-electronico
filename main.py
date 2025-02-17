import all_pages
import theme
import os
from utils.window_manager import WindowMgr, set_window_icon
from nicegui import app, ui
import tkinter as tk

from database import Base, engine


FAVICON_PATH = os.path.join("static", "favicon.ico")
WINDOW_TITLE="UPIITA - Expediente electrónico"

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

set_window_icon(FAVICON_PATH, WINDOW_TITLE)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)



# this call shows that you can also move the whole page creation into a separate file
all_pages.create()

app.native.start_args['icon'] = FAVICON_PATH

ui.run(title=WINDOW_TITLE, favicon=FAVICON_PATH, native=True, window_size=(screen_width, screen_height))
