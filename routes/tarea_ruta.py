from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from chromadb.errors import InvalidCollectionException
from schemas.tarea import Tarea
from config.db import crear_conexion
from models.tarea import crear_tarea

tareas = APIRouter()
metadata_coleccion = ["tarea", "Esta colección contendrá la tarea que el usuario inserte."]


# Creando el endpoint GET '/tareas'
@tareas.get('/tareas', response_class=JSONResponse, tags=["tareas"])
def get_tareas():
    try:
        client = crear_conexion()
        collection = client.get_collection(name="tareas")
        
        return {
            "respuesta": collection
        }

    except InvalidCollectionException as ice:
        return {
            "mensaje": "No hay colecciones"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ha ocurrido un error inesperado en el servidor. Inténtelo de nuevo."
        )


# Creando el endpoint POST '/tareas'
@tareas.post('/tareas', tags=["tareas"])
def post_tareas(tarea: Tarea):
    try:
        data = dict(tarea)
        
        crear_tarea(
            metadata_coleccion[0], metadata_coleccion[1],
            data["id"], data["titulo"], data["descripcion"], data["estado"]
        )
        
        return data
    
    except Exception as e:
        raise e