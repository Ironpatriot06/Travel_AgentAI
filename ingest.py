import os
import requests
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

os.environ["GOOGLE_API_KEY"] = "AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
persist_directory = "vector_db/blogs"
documents = []

with open("urls.txt") as f:
    urls = [line.strip() for line in f.readlines()]

for url in urls:
    try:
        loader = WebBaseLoader(url)
        data = loader.load()
        documents.extend(data)
    except Exception as e:
        print(f"Failed to load {url}: {e}")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

Chroma.from_documents(
    docs,
    embedding=embedding,
    persist_directory=persist_directory
)
print("✅ Ingestion complete.")
