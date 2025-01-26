from chromadb import Collection


def contador(coleccion: Collection) -> int:
    # Consulta todos los items de la base de datos vectorial y con ello, su longitud para el siguiente ID
    cant_tareas = len(coleccion.get()['documents'])
    print(f"Cantidad de items: {cant_tareas}")
    return cant_tareas