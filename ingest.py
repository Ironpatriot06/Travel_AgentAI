import os
import time
import requests
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Set API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"

# Set User-Agent
os.environ["USER_AGENT"] = "travel-agent/1.0"

# Embeddings
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
persist_directory = "vector_db/blogs"

# Load URLs
with open("urls.txt") as f:
    urls = [line.strip() for line in f if line.strip()]

documents = []

# Fetch with timeout protection
for url in urls:
    print(f"🔄 Loading: {url}")
    try:
        loader = WebBaseLoader(url)
        data = loader.load()
        documents.extend(data)
    except Exception as e:
        print(f"❌ Failed to load {url}: {e}")
    time.sleep(1)  # be polite to servers

# Split & Embed
print("✂️ Splitting documents...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

print(f"📚 Total chunks: {len(docs)}")
if not docs:
    print("⚠️ No documents to embed. Exiting.")
    exit()

print("📦 Creating vector DB...")
Chroma.from_documents(
    docs,
    embedding=embedding,
    persist_directory=persist_directory
)

print("✅ Ingestion complete.")

