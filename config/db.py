# Importando los paquetes necesarios
from chromadb import Client, PersistentClient, Collection
from chromadb.config import Settings
from chromadb.errors import AuthorizationError, ChromaAuthError, ChromaError, InternalError, NotFoundError
from datetime import datetime


client = None

def crear_conexion(path: str='./data/chromadb', telemetry: bool=False) -> Client:
    global client
    
    try:
        if client is None:
            client = PersistentClient(
                path=path,
                settings=Settings(
                    anonymized_telemetry=telemetry
                )
            )
            print("Se ha creado una nueva instancia de ChromaDB Client.")
        
        else:
            print("Se reutiliza la instancia existente de ChromaDB Client.")
        
        
        client.heartbeat()
        print("Conexión exitosa a ChromaDB!!")
        return client
    
    except ValueError as ve:
        print(f"Configuración inválida: {ve}")
    
    except FileNotFoundError as fnfe:
        print(f"El directorio de persistencia no existe: {fnfe}")
    
    except PermissionError as pe:
        print(f"No se tienen permisos para el directorio: {pe}")
    
    except AuthorizationError as ae:
        print(f"No se ha podido autorizar la petición correctamente: {ae}")
    
    except ChromaAuthError as cae:
        print(f"No se ha podido autenticar correctamente: {cae}")
    
    except InternalError as ie:
        print(f"Ha ocurrido un error interno en el servidor: {ie}")
    
    except NotFoundError as nfe:
        print(f"El recurso solicitado no ha sido encontrado: {nfe}")
    
    except ChromaError as ce:
        print("Algo ha ido mal en el servidor de Chroma. Inténtelo de nuevo más tarde o comuníquese con un administrador si el problema continúa.")
        print(f"Error: {ce}")
    
    except Exception as e:
        print("Ha ocurrido un error inesperado. Imposible continuar. Inténtelo de nuevo más tarde o comuníquese con un administrador si el problema persiste.")
        print(f"Error: {e}")


def crear_coleccion(
    nombre: str,
    descripcion: str,
    space: str="cosine",
    search_construction_ef: int=400,
    num_threads: int=4
) -> Collection:
    try:
        if not nombre.strip():
            raise ValueError("El nombre de la colección no puede estar vacío.")

        if search_construction_ef <= 0 or num_threads <= 0:
            raise ValueError("Los parámetros 'search_construction_ef' y 'num_threads' deben ser mayores a 0.")
        
        crear_conexion()
        
        
        colecciones = client.list_collections() 
        if nombre in colecciones:
            print(f"La colección '{nombre}' ya existe.")
            return client.get_collection(name=nombre)
        
        
        # Crear colección
        tarea = client.create_collection(
            name=nombre,
            metadata={
                "descripcion": descripcion,
                "creado": str(datetime.now()),
                "hnsw:space": space,
                "hnsw:search_ef": search_construction_ef,
                "hnsw:construction_ef": search_construction_ef,
                "hnsw:num_threads": num_threads
            }
        )
        
        print(f"Colección '{nombre}' creada exitosamente!!")
        return tarea
    
    except ChromaError as ce:
        print(f"Error con el gestor de base de datos ChromaDB: {ce}")
        raise ChromaError(ce)
    
    except Exception as e:
        print(f"Se ha producido un error al crear la colección: {e}")
        raise Exception(e)