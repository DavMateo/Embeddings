from typing import Optional
from pydantic import BaseModel


# Revisar comportamiento
class Tarea(BaseModel):
    id: Optional[str] = None   #Revisar comportamiento. Como alternativa, colocar el "autoincrement" aquí.
    titulo: str
    descripcion: str
    estado: bool