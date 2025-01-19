import chromadb
from chromadb.config import Settings
from datetime import datetime

client = chromadb.Client(settings=Settings(anonymized_telemetry=False,persist_directory='./data'))


collection = client.create_collection(
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


collection.add(
    documents=[
        str({"campo1": "texto1"})
    ],
    metadatas=[{"meta": "data"}],
    ids=["id1"]
)

result = collection.get(ids=["id1"])
print(result)