import os
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# 🔐 API key
os.environ["GOOGLE_API_KEY"] = "your_api_key"
os.environ["USER_AGENT"] = "RatishKapoorBot/1.0"

# 🧠 Load vector DB
persist_directory = "vector_db/blogs"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# 🤖 Gemini Pro LLM
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-002", temperature=0.4)
# 💬 Memory for context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

# 🔍 Conversational chain with retriever
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(),
    memory=memory,
    return_source_documents=True,
    output_key="answer"  # 👈 This resolves the error
)

# 🌐 Streamlit UI
st.set_page_config(page_title="Dubai Travel Chatbot 💬", layout="centered")
st.title("🧳 Dubai Itinerary Planner Chatbot")
st.markdown("Chat with an AI assistant to plan your personalized trip to Dubai!")

# 💾 Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "preferences" not in st.session_state:
    st.session_state.preferences = {
        "dates": None,
        "interests": [],
        "duration": None
    }

if "planning" not in st.session_state:
    st.session_state.planning = False

# 🚀 Chat Interface
user_input = st.chat_input("Ask me anything about Dubai...")

if user_input:
    try:
        # Invoke QA chain
        response = qa_chain.invoke({"question": user_input})
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
    except Exception as e:
        st.error("Sorry, there was an issue answering your question. Please try again.")
        st.exception(e)

# 💬 Display chat messages
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

