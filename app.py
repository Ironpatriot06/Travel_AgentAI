import os
import re
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma

# 🔐 API Key
os.environ["GOOGLE_API_KEY"] = "your_api_key"

# 📚 Load Vector DB
persist_directory = "vector_db/blogs"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever = vectordb.as_retriever(search_kwargs={"k": 8})

# 🎯 Custom Prompt Template
custom_prompt = PromptTemplate(
    input_variables=["chat_history", "question", "context"],
    template="""
You are a helpful Dubai travel planning assistant.

Use the following travel blog content:
{context}

Conversation so far:
{chat_history}

User asked:
{question}

If the user hasn't mentioned how many days they're staying, politely ask them.
If days and child age are mentioned, generate a personalized itinerary with activities that suit their stay and the child’s age.
Be concise, realistic, and helpful.
"""
)

# 🤖 LLM
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-002", temperature=0.4)

# 🧠 Memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer"
   )

memory = st.session_state.memory

# 🔗 QA Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": custom_prompt},
    output_key="answer"
)

# 🌐 Streamlit UI
st.title("🧳 Dubai Travel Assistant")

# 🧠 Init session state
if "days" not in st.session_state:
    st.session_state.days = None
if "kid_age" not in st.session_state:
    st.session_state.kid_age = None

# 🧪 Extraction helpers
def extract_days(text):
    match = re.search(r"(\d+)\s*(day|days|night|nights)", text.lower())
    if match:
        return int(match.group(1))
    return None

def extract_kid_age(text):
    match = re.search(r"(\d+)\s*(year|years)\s*old", text.lower())
    if match:
        return int(match.group(1))
    return None

# 📩 User input
user_input = st.text_input("Ask me about your Dubai trip:")

if user_input:
    # Extract and store values
    extracted_days = extract_days(user_input)
    if extracted_days is not None:
        st.session_state.days = extracted_days

    extracted_kid_age = extract_kid_age(user_input)
    if extracted_kid_age is not None:
        st.session_state.kid_age = extracted_kid_age

    # Add facts if known
    contextual_question = user_input
    if st.session_state.days:
        contextual_question += f"\nNote: The user is staying for {st.session_state.days} days."
    if st.session_state.kid_age:
        contextual_question += f"\nNote: The user has a {st.session_state.kid_age}-year-old child."

    # Answer
    response = qa_chain.run(question=contextual_question)
    st.write(response)

