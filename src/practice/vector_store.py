import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = [
    "Python is a programming language.",
    "Machine learning uses data.",
    "Cats are animals."
]
embeddings = model.encode(chunks)
print(embeddings.shape)

dimensions = embeddings.shape[1] #384
index = faiss.IndexFlatL2(dimensions) #This creates a simple FAISS index.
index.add(embeddings)

query = "What is machine learning?"
query_embedding = model.encode([query]) #Why the square brackets? Because model.encode() can process multiple texts at once. Passing a list ensures the output has the correct shape for FAISS.
distances, indices = index.search(query_embedding,k=2)

print(distances)
print(indices)

for i in indices[0]:
    print(chunks[i])

context = ""

for i in indices[0]:
    context += chunks[i] + "\n"

print(context)