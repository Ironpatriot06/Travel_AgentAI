from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import requests
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"
os.environ["USER_AGENT"] = "RatishKapoorBot/1.0"

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def is_url_valid(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def extract_main_content(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main_content = soup.find("div", class_="entry-content") or soup.find("article")
    return main_content.get_text(separator="\n", strip=True) if main_content else soup.get_text(separator="\n", strip=True)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def ingest_multiple_blogs_to_vectorstore(urls, persist_dir="vector_db/blogs"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_docs = []

    for url in urls:
        print(f"\n🌐 Loading URL: {url}")
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            print(f"✅ Loaded {len(docs)} documents")

            if docs and docs[0].page_content.strip():
                split_docs = splitter.split_documents(docs)
                print(f"📄 Split into {len(split_docs)} chunks")
                all_docs.extend(split_docs)
            else:
                print("⚠️ No content found on page.")

        except Exception as e:
            print(f"❌ Failed to load {url}: {e}")

    if all_docs:
        print(f"\n🔐 Storing {len(all_docs)} total chunks in Chroma DB...")
        vectordb = Chroma.from_documents(all_docs, embedding=embeddings, persist_directory=persist_dir)
        vectordb.persist()
        print("✅ All blogs ingested and stored successfully.")
    else:
        print("🚫 No data was ingested. Check URLs and content.")

def search_blog(query, persist_dir="vector_db/blogs"):
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    results = vectordb.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in results])

