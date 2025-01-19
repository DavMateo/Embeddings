from sentence_transformers import SentenceTransformer
from typing import List, Union

def initModel(nombre: str) -> SentenceTransformer:
    try:
        model = SentenceTransformer(nombre)
        return model
    
    except Exception as e:
        raise ValueError(f"No se pudo cargar el modelo '{nombre}': {e}")

def vectorizar(lstWords: List, nombre: str) -> List[List[float]]:
    if not isinstance(lstWords, list):
        raise ValueError("La entrada 'lstWords' debe ser una lista.")
    
    if not all(isinstance(word, str) for word in lstWords):
        raise ValueError("Todos los elementos de 'lstWords deben ser cadenas de texto.")
    
    try:
        model = initModel(nombre)
        lstFinal = model.encode(lstWords)
        return lstFinal
    
    except Exception as e:
        raise RuntimeError(f"Error al vectorizar las palabras {e}")