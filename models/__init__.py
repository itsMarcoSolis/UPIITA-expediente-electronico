from sqlalchemy.orm import configure_mappers
from .alumno import Alumno
from .asociacion import Asociacion
from .grupo import Grupo
from .miembro_asociacion import MiembroAsociacion
from .miembro_grupo import MiembroGrupo
from models.archivo import Archivo
from models.grafico import Grafico

configure_mappers()
