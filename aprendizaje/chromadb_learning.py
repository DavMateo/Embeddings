# Crear un cliente de ChromaDB
import chromadb
from chromadb.config import Settings
from datetime import datetime
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.PersistentClient(path="./data", settings=Settings(anonymized_telemetry=False))
chroma_client.heartbeat()


def initModel(nombre):
    return SentenceTransformer(nombre)

def vectorizar(lstWords):
    model = initModel("sentence-transformers/all-MiniLM-L6-v2")
    lstFinal = []
    
    for word in lstWords:
        lstFinal.append(model.encode(word))

    return lstFinal



# Crear una colección
"""Explicación ChromaDB
    ChromaDB es una base de datos no relacional. Aquí, las colecciones son el equivalente a las
    tablas de una base de datos relacional. Cada colección almacenará documentos, que su equivalente
    sería a un atributo.
"""
collection = chroma_client.create_collection(
    name="myCollection",
    metadata={
        "descripcion": "Mi primera colección de Chroma",
        "creado": str(datetime.now()),
        "hnsw:space": "cosine",
        "hnsw:search_ef": 400,
        "hnsw:construction_ef": 400,
        "hnsw:num_threads": 8
    }
)

# Agregando documentos a la colección
collection.add(
    documents=[
        "Esto es un documento sobre una piña",
        "Esto es un documento sobre naranjas"
    ],
    ids=["id1", "id2"]
)

# Consultas a la colección
"""Explicación ChromaDB
    Una consulta está compuesta por dos campos, el o los textos de consulta que luego# Eliminando una colección
chroma_client.delete_collection(name="test")
chroma_client.delete_collection(name="myCollection") serán embebidos para
    relacionarse con la información guardada en la base de datos buscando coincidencias, y la cantidad de
    resultados a devolver, que por defecto son los 10 mejores resultados a la consulta hecha.
"""
results = collection.query(
    query_texts=["Esto es un documento sobre Florida"],  #Se le aplicará embeddings
    n_results=2  #Cantidad de resultados a devolver
)
# print(results)


# Obtener un documento
collection = chroma_client.get_collection(name="myCollection")

# Obtener o crear un documento si no existe
collection = chroma_client.get_or_create_collection(name="test")

# Devuelve una lista de los primeros 10 elementos de la colección
collection.peek()

# Devuelve el número de artículos en la colección
collection.count()

# Cambia el nombre de la colección
collection.modify(name="nuevo_nombre")




# Agregando información en bruto a Chroma
lstPalabras = ["lorem ipsum...", "doc2", "doc3"]
collection.add(
    documents=lstPalabras,
    metadatas=[
        {"capitulo": "3", "verso": "16"},
        {"capitulo": "3", "verso": "5"},
        {"capitulo": "29", "verso": "11"}
    ],
    ids=["id1", "id2", "id3"]
)


# Agregando los embeddings vectorizados en la base de datos
"""Explicación ChromaDB
    Debido a que permite el almacenamiento de embeddings directamente en la base de datos,
    se puede hacer que solo se guarden los vectores y mediante sus respectivos identificadores
    asociados durante la creación de la tabla, enlazar esa colección con otra colección donde es donde
    se almacena los documentos guardados sin vectorizarlo explícitamente.
"""

lstPalabras1 = ["documento1", "documento2", "documento3"]
lstVector = vectorizar(lstPalabras1)

collection.add(
    documents=lstPalabras1,
    embeddings=[
        lstVector[0],
        lstVector[1],
        lstVector[2]
    ],
    metadatas=[
        {"capitulo": "3", "verso": "16"},
        {"capitulo": "3", "verso": "5"},
        {"capitulo": "29", "verso": "11"}
    ],
    ids=["id1", "id2", "id3"]
)


# Actualizando los datos PRESENTES en una colección
lstPalabras2 = ["doc1", "doc2", "doc3"]
lstVector = vectorizar(lstPalabras2)

collection.update(
    ids=["id1", "id2", "id3"],
    embeddings=[
        lstVector[0],
        lstVector[1],
        lstVector[2]
    ],
    metadatas=[
        { "capitulo": "6", "verso": "16" },
        { "capitulo": "3", "verso": "5" },
        { "capitulo": "76", "verso": "43" }
    ],
    documents=["doc1", "doc2", "doc3"]
)


# Actualizando y/o creando los datos presentes y nuevos en una colección
collection.upsert(
    ids=["id1", "id2", "id3"],
    embeddings=[
        lstVector[0],
        lstVector[1],
        lstVector[2]
    ],
    metadatas=[
        { "capitulo": "6", "verso": "16" },
        { "capitulo": "3", "verso": "5" },
        { "capitulo": "76", "verso": "43" }
    ],
    documents=["doc1", "doc2", "doc3"]
)


# Eliminando información desde las colecciones de Chroma
# IMPORTANTE: TODA LA INFORMACIÓN ELIMINADA, NO PODRÁ RECUPERARSE LUEGO.
collection.delete(
    ids=["id1", "id2", "id3"],
    where={"capitulo": "20"}
)


# Realizando consultas a la base de datos
lst_test = vectorizar(["doc2"])

resultado = collection.query(
    query_embeddings=[ lst_test[0] ],
    n_results=2
)
print(resultado)
print("\n")


# Realizando consultas a la base de datos mediante texto normal
resultado_con_texto = collection.query(
    query_texts=["doc1"],
    n_results=2
)
print(resultado_con_texto)
print("\n")


"""Explicación ChromaDB
    Se pueden realizar consultas de dos maneras: usando 'query_embeddings' que consiste en pasarle el texto de las
    consultas deseadas ya vectorizadas, o usar 'query_texts' que recibe el texto como string y ChromaDB se encarga
    de realizar la respectiva conversión a vectores para continuar con el mismo flujo de consulta que 'query_embeddings'.
"""


# Obteniendo información usando resultados de consultas previas
obtener_resultado = collection.get(
    include=["documents"]
)
print(obtener_resultado)
print("\n")

consulta_resultado = collection.query(
    query_texts=["doc3"],
    n_results=2,
    include=["documents"]
)
print(consulta_resultado)
print("\n")


# Filtrado de metadata usando condicionales
consulta_metadata = collection.get(
    where={
        "$and": [
            {
                "capitulo": {
                    "$ne": "76"
                }
            },
            {
                "verso": {
                    "$eq": "16"
                }
            }
        ]
    }
)
print(consulta_metadata)
print("\n")


"""Explicación ChromaDB
    ChromaDB es multimodal, por lo que permite insertar imágenes como arrays de numpy en las colecciones que deseemos crear. 
    Esto implica que no solo se puede agregar texto e imágenes (Archivo o URI), sino que también permite consultar y 
    actualizar colecciones y documentos usando texto e imágenes también, lo cuál le da un potencial en la manera en como se
    gestiona la información partiendo de un modelo vectorial que interpreta los sistemas de IA.
"""