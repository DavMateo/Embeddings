import chromadb
from chromadb import Settings, Collection
from chromadb.errors import ChromaAuthError, ChromaError
from datetime import datetime

PATH = "./data"


def config_inicial(
    nombre: str,
    descripcion: str,
    space: str="cosine",
    search_construction_ef: int=400,
    num_threads: int=4
) -> list:
    global client
    
    try:
        # Estableciendo y verificando la conexión a la DB
        client = chromadb.PersistentClient(path=PATH, settings=Settings(anonymized_telemetry=False))
        client.heartbeat()
        
        # Creando u obteniendo la colección "tareas"
        coleccion = client.get_or_create_collection(
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
        
        # Retorno tanto el cliente como la colección, para ello lo encapsulo en una lista
        print("Creación u obtención de la colección realizado con éxito!!")
        return [client, coleccion]
        
    # Manejo de las excepciones que puedan ocurrir durante la ejecución del programa.
    except FileNotFoundError as fnfe:
        print("Error en la configuración del directorio de la base de datos especificada.")
        raise FileNotFoundError(str(fnfe))

    except PermissionError as pe:
        print("Error en los permisos de lectura y escritura del directorio de la DB.")
        raise PermissionError(str(pe))
    
    except ChromaAuthError as cae:
        print("Error de autenticación.")
        raise ChromaAuthError(str(cae))
    
    except ChromaError as ce:
        print("Algo ha ido mal con la base de datos de ChromaDB. Inténtelo de nuevo más tarde o comuníquese con un administrador.")
        raise ChromaError(str(ce))
    
    except Exception as e:
        print("Ha ocurrido un error inesperado. Imposible continuar. Inténtelo de nuevo más tarde o comuníquese con un administrador.")
        raise Exception(str(e))