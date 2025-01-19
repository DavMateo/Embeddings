import chromadb
from config.db import crear_coleccion, client
from utils.iniciarModelo import vectorizar
from datetime import datetime

def crear_tarea(
    nombre: str,
    descripcion_tabla: str,
    id: str,
    titulo: str,
    descripcion: str,
    estado: bool
):
    collection = crear_coleccion(nombre, descripcion_tabla)
    
    try:
        collection.add(
            documents=[
                str({
                    "titulo": titulo,
                    "descripcion": descripcion
                })
            ],
            metadatas=[
                {
                    "id": id,
                    "fecha_creacion": str(datetime.now()),
                    "estado": estado
                }
            ],
            ids=[id]
        )
    
    except Exception as e:
        print(f"Error durante ejecución: {e}")
    
    print(collection.get())