# Importando las librerías necesarias
from typing import Optional
from pydantic import BaseModel
from utils.autoincrementador import obtener_siguiente_id

class Tarea(BaseModel):
    id: Optional[str] = obtener_siguiente_id()
    titulo: str
    descripcion: str
    estado: bool