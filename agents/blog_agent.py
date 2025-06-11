# agents/blog_agent.py

import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma as LCChroma  # Alias if using langchain.vectorstores also


os.environ["GOOGLE_API_KEY"] = "your_api_key"
os.environ["USER_AGENT"] = "RatishKapoorBot/1.0"

# ✅ Embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# ✅ Check if a URL is valid and reachable
def is_url_valid(url):
    try:
        headers = {"User-Agent": "RatishKapoorBot/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

# ✅ Load and chunk blog content
def chunk_blog_urls(urls, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = []
    for url in urls:
        try:
            print(f"🌐 Loading: {url}")
            loader = WebBaseLoader(url, header_template={"User-Agent": "RatishKapoorBot/1.0"})
            docs = loader.load()
            if docs:
                chunks = splitter.split_documents(docs)
                all_chunks.extend(chunks)
                print(f"✅ Loaded {url} -> {len(chunks)} chunks")
            else:
                print(f"⚠️ No content from {url}")
        except Exception as e:
            print(f"❌ Error loading {url}: {e}")
    return all_chunks

# ✅ Ingest blogs and save to Chroma vector DB
def ingest_multiple_blogs_to_vectorstore(urls, persist_dir="vector_db/blogs"):
    chunks = chunk_blog_urls(urls)
    if not chunks:
        print("❌ No chunks were created. Check URLs or scraping.")
        return

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    print(f"✅ Vectorstore created with {len(chunks)} chunks and saved to '{persist_dir}'")

# ✅ Search from the vector DB
def search_blog(query, persist_dir="vector_db/blogs"):
    if not query.strip():
        return "❌ Empty query."

    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    results = vectordb.similarity_search(query, k=5)
    if not results:
        return "❌ No relevant results found."

    return [r.page_content for r in results]

