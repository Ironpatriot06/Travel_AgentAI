from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory="vector_db/blogs", embedding_function=embedding)

# Get the raw documents that were embedded
docs = vectordb.get()["documents"]

# Search for the word "Savi"
for i, doc in enumerate(docs):
    if "savi" in doc.lower():
        print(f"--- Match in chunk {i} ---")
        print(doc)
        print()

