from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "documento1",
    "documento2",
    "documento3"
]
embeddings = model.encode(sentences)
print(embeddings)

#similarities = model.similarity(embeddings, embeddings)
#print(similarities.shape)
# [4, 4]