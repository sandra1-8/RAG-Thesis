# # loading pdf

# from pypdf import PdfReader
# reader = PdfReader("data/sample.pdf")
# print(len(reader.pages))
# first_page = reader.pages[0]
# text = first_page.extract_text()
# print(text)

# # chunking

# def chunk_text(text,chunk_size):
#     chunks = []

#     for i in range(0,len(text),chunk_size):
#         chunk = text[i:i+chunk_size]
#         chunks.append(chunk)

#     return chunks

# c = chunk_text(text,100)
# print(c)

# embedding

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("machine learning is amazing")
print(type(embedding))
print(len(embedding))
print(embedding[:10])