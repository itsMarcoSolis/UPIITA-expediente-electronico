from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

#  Modelo de Alumno
class AlumnoBase(BaseModel):
    id: int
    boleta: str
    nombre: str
    correo: Optional[str] = None
    fecha_registro: datetime

class AlumnoCreate(BaseModel):
    boleta: str
    nombre: str
    correo: Optional[str] = None

#  Modelo de Asociación
class AsociacionBase(BaseModel):
    id: int
    nombre: str
    asesor: str
    foto_asesor: Optional[str] = None

class AsociacionCreate(BaseModel):
    nombre: str
    asesor: str
    foto_asesor: Optional[str] = None

#  Modelo de Grupo
class GrupoBase(BaseModel):
    id: int
    nombre_grupo: str
    asociacion_id: int

class GrupoCreate(BaseModel):
    nombre_grupo: str
    asociacion_id: int

#  Modelo de Miembros de Asociaciones
class MiembroAsociacionBase(BaseModel):
    id: int
    alumno_id: int
    asociacion_id: int

class MiembroAsociacionCreate(BaseModel):
    alumno_id: int
    asociacion_id: int

#  Modelo de Miembros de Grupos
class MiembroGrupoBase(BaseModel):
    id: int
    alumno_id: int
    grupo_id: int
    fecha_ingreso: datetime

class MiembroGrupoCreate(BaseModel):
    alumno_id: int
    grupo_id: int
