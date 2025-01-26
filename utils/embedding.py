from sentence_transformers import SentenceTransformer

def generar_embedding(texto: str):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return model.encode(texto).tolist()